"""
Routes /api/reports — Logique principale de génération de rapports
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Optional

from services.openai_service import generate_narrative, generate_kpi_summary, generate_chart_config
from services.searxng_service import build_context_for_report
from services.qdrant_service import save_report, search_similar_reports, get_all_reports, get_report_by_id
from services.data_service import get_demo_data, detect_report_type

router = APIRouter()


class GenerateRequest(BaseModel):
    name: str
    type: str
    data: dict[str, Any]
    use_web_search: bool = True
    save_to_memory: bool = True
    extra_instructions: str = ""


class SearchRequest(BaseModel):
    query: str
    report_type: Optional[str] = None


@router.post("/generate")
async def generate_report(req: GenerateRequest):
    """
    Génère un rapport complet :
    1. Enrichit avec SearxNG (web search)
    2. Génère narratif via GPT-4o
    3. Génère KPIs structurés
    4. Génère configs Chart.js
    5. Sauvegarde dans Qdrant
    """
    report_id = str(uuid.uuid4())

    # 1. Contexte web (SearxNG)
    search_context = ""
    if req.use_web_search:
        try:
            search_context = await build_context_for_report(req.type, req.name, req.data)
        except Exception as e:
            print(f"⚠️ SearxNG skip: {e}")

    # 2. Narratif GPT-4o
    try:
        narrative = await generate_narrative(
            report_type=req.type,
            data=req.data,
            report_name=req.name,
            search_context=search_context,
            extra_instructions=req.extra_instructions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération narratif: {e}")

    # 3. KPIs structurés
    kpis = []
    try:
        kpi_result = await generate_kpi_summary(req.data, req.type)
        kpis = kpi_result.get("kpis", [])
    except Exception as e:
        print(f"⚠️ KPI generation skip: {e}")

    # 4. Charts config
    charts = []
    try:
        charts = await generate_chart_config(req.data, req.type)
    except Exception as e:
        print(f"⚠️ Charts generation skip: {e}")

    # 5. Construction du rapport final
    report = {
        "report_id": report_id,
        "name": req.name,
        "type": req.type,
        "data": req.data,
        "narrative": narrative,
        "kpis": kpis,
        "charts": charts,
        "search_context_used": bool(search_context),
    }

    # 6. Sauvegarde Qdrant
    if req.save_to_memory:
        try:
            await save_report(report_id, report)
        except Exception as e:
            print(f"⚠️ Qdrant save skip: {e}")

    return report


@router.get("/demo/{report_type}")
async def get_demo_report(report_type: str):
    """Charge les données de démo pour un type de rapport."""
    demo = get_demo_data(report_type)
    if not demo:
        raise HTTPException(status_code=404, detail=f"Type '{report_type}' inconnu")
    return demo


@router.get("/history")
async def get_report_history():
    """Retourne l'historique des rapports depuis Qdrant."""
    try:
        reports = await get_all_reports(limit=20)
        return {"reports": reports, "count": len(reports)}
    except Exception as e:
        return {"reports": [], "count": 0, "error": str(e)}


@router.post("/search")
async def search_reports(req: SearchRequest):
    """Recherche des rapports similaires dans Qdrant."""
    try:
        results = await search_similar_reports(req.query, req.report_type)
        return {"results": results}
    except Exception as e:
        return {"results": [], "error": str(e)}


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Récupère un rapport spécifique depuis Qdrant."""
    report = await get_report_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return report
