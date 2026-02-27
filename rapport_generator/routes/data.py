"""
Routes /api/data — Upload et ingestion de fichiers (CSV, JSON)
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Any

from services.data_service import parse_csv, parse_json, normalize_uploaded_data, detect_report_type
from services.openai_service import extract_structured_data

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload et parse un fichier CSV ou JSON."""
    content = await file.read()
    content_str = content.decode("utf-8", errors="replace")
    filename = file.filename or "fichier"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    try:
        if ext == "csv":
            raw_data = parse_csv(content_str)
        elif ext == "json":
            raw_data = parse_json(content_str)
        else:
            # Tenter JSON d'abord, sinon CSV
            try:
                raw_data = parse_json(content_str)
            except Exception:
                try:
                    raw_data = parse_csv(content_str)
                except Exception:
                    raise HTTPException(status_code=400, detail="Format de fichier non reconnu (CSV ou JSON attendu)")

        normalized = normalize_uploaded_data(raw_data, filename)
        return {
            "success": True,
            "filename": filename,
            "detected_type": normalized.get("type"),
            "data": normalized,
            "preview": str(raw_data)[:500],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de parsing: {e}")


class ExtractRequest(BaseModel):
    raw_text: str
    report_type: str = "generic"


@router.post("/extract")
async def extract_from_text(req: ExtractRequest):
    """Extrait des données structurées depuis du texte brut via GPT."""
    try:
        structured = await extract_structured_data(req.raw_text, req.report_type)
        return {
            "success": True,
            "extracted_data": structured,
            "detected_type": detect_report_type(structured),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur extraction: {e}")


class ManualDataRequest(BaseModel):
    name: str
    type: str
    data: dict[str, Any]


@router.post("/validate")
async def validate_data(req: ManualDataRequest):
    """Valide et normalise des données saisies manuellement."""
    from services.data_service import normalize_uploaded_data
    normalized = normalize_uploaded_data(req.data, req.name)
    normalized["type"] = req.type
    normalized["name"] = req.name
    return {"valid": True, "data": normalized}
