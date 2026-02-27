"""
Service Qdrant — Stockage vectoriel des rapports (mémoire persistante)
"""
import json
import uuid
import hashlib
from datetime import datetime
from typing import Any, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter,
    FieldCondition, MatchValue, SearchRequest
)
from openai import AsyncOpenAI

from config import settings

# Clients
qdrant = AsyncQdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

VECTOR_SIZE = 1536  # text-embedding-3-small
COLLECTION = settings.QDRANT_COLLECTION


async def ensure_collection():
    """Crée la collection Qdrant si elle n'existe pas."""
    try:
        collections = await qdrant.get_collections()
        names = [c.name for c in collections.collections]
        if COLLECTION not in names:
            await qdrant.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )
            print(f"✅ Collection Qdrant '{COLLECTION}' créée")
        return True
    except Exception as e:
        print(f"⚠️ Qdrant non disponible: {e}")
        return False


async def embed_text(text: str) -> list[float]:
    """Génère un embedding via OpenAI."""
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000],  # limite token
    )
    return response.data[0].embedding


async def save_report(report_id: str, report_data: dict) -> bool:
    """Sauvegarde un rapport dans Qdrant avec son embedding."""
    try:
        await ensure_collection()

        # Texte représentatif pour l'embedding
        embed_input = f"{report_data.get('name', '')} {report_data.get('type', '')} {report_data.get('narrative', '')[:500]}"
        vector = await embed_text(embed_input)

        payload = {
            "report_id": report_id,
            "name": report_data.get("name", "Sans titre"),
            "type": report_data.get("type", "generic"),
            "created_at": datetime.now().isoformat(),
            "narrative_preview": report_data.get("narrative", "")[:300],
            "data_summary": json.dumps(report_data.get("data", {}), ensure_ascii=False)[:500],
            "full_data": json.dumps(report_data, ensure_ascii=False)[:10000],
        }

        point_id = int(hashlib.md5(report_id.encode()).hexdigest()[:8], 16)

        await qdrant.upsert(
            collection_name=COLLECTION,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )
        return True
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde Qdrant: {e}")
        return False


async def search_similar_reports(query: str, report_type: Optional[str] = None, limit: int = 5) -> list[dict]:
    """Recherche des rapports similaires par similarité vectorielle."""
    try:
        await ensure_collection()
        vector = await embed_text(query)

        filters = None
        if report_type:
            filters = Filter(
                must=[FieldCondition(key="type", match=MatchValue(value=report_type))]
            )

        results = await qdrant.search(
            collection_name=COLLECTION,
            query_vector=vector,
            query_filter=filters,
            limit=limit,
            with_payload=True,
        )

        return [
            {
                "score": round(r.score, 3),
                "name": r.payload.get("name"),
                "type": r.payload.get("type"),
                "created_at": r.payload.get("created_at"),
                "preview": r.payload.get("narrative_preview"),
                "report_id": r.payload.get("report_id"),
            }
            for r in results
        ]
    except Exception as e:
        print(f"⚠️ Erreur recherche Qdrant: {e}")
        return []


async def get_all_reports(limit: int = 20) -> list[dict]:
    """Récupère tous les rapports stockés."""
    try:
        await ensure_collection()
        results, _ = await qdrant.scroll(
            collection_name=COLLECTION,
            limit=limit,
            with_payload=True,
        )
        return [
            {
                "name": r.payload.get("name"),
                "type": r.payload.get("type"),
                "created_at": r.payload.get("created_at"),
                "report_id": r.payload.get("report_id"),
            }
            for r in results
        ]
    except Exception as e:
        print(f"⚠️ Erreur lecture Qdrant: {e}")
        return []


async def get_report_by_id(report_id: str) -> Optional[dict]:
    """Récupère un rapport spécifique."""
    try:
        results, _ = await qdrant.scroll(
            collection_name=COLLECTION,
            scroll_filter=Filter(
                must=[FieldCondition(key="report_id", match=MatchValue(value=report_id))]
            ),
            limit=1,
            with_payload=True,
        )
        if results:
            payload = results[0].payload
            full = payload.get("full_data", "{}")
            return json.loads(full)
        return None
    except Exception as e:
        print(f"⚠️ Erreur get rapport: {e}")
        return None
