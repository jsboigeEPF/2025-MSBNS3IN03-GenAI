"""
Routes /api/export — Génération et téléchargement de PDF
"""
import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Any

from services.pdf_service import generate_pdf
from config import settings

router = APIRouter()


class ExportRequest(BaseModel):
    report_id: str = ""
    name: str
    type: str
    narrative: str
    data: dict[str, Any]
    kpis: list[dict] = []


@router.post("/pdf")
async def export_pdf(req: ExportRequest):
    """Génère un PDF et retourne le lien de téléchargement."""
    safe_name = "".join(c for c in req.name if c.isalnum() or c in " -_").strip().replace(" ", "_")
    filename = f"{safe_name}_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(settings.EXPORT_DIR, filename)

    try:
        generate_pdf(
            report_name=req.name,
            report_type=req.type,
            narrative=req.narrative,
            data=req.data,
            kpis=req.kpis,
            output_path=output_path,
        )
        return {
            "success": True,
            "filename": filename,
            "download_url": f"/api/export/download/{filename}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération PDF: {e}")


@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """Télécharge un PDF généré."""
    # Sécurité : pas de path traversal
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide")

    filepath = os.path.join(settings.EXPORT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
