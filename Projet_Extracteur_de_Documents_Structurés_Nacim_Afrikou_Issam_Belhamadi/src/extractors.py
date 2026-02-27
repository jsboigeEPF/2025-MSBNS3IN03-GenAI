"""Pipeline d'extraction de données depuis des fichiers non structurés via Structured Outputs."""

from pathlib import Path
from typing import Optional

import pdfplumber
try:
    from docx import Document
except ImportError:
    Document = None

try:
    import pandas as pd
except ImportError:
    pd = None

from .llm_client import detect_document_type, extract_invoice_with_llm, extract_order_with_llm
from .models import ExtractedDocument, Invoice, Order


def _extract_text_from_pdf(path: Path) -> str:
    """Lit et concatène le texte de toutes les pages d'un PDF."""
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def _extract_text_from_docx(path: Path) -> str:
    """Extrait le texte d'un fichier Word (.docx)."""
    if Document is None:
        raise RuntimeError("python-docx non installé. Exécutez : pip install python-docx")
    doc = Document(path)
    return "\n".join(para.text for para in doc.paragraphs)


def _extract_text_from_excel(path: Path) -> str:
    """Extrait le texte d'un fichier Excel (.xlsx, .xls)."""
    if pd is None:
        raise RuntimeError("pandas non installé. Exécutez : pip install pandas openpyxl")
    df = pd.read_excel(path, sheet_name=None)  # Lit toutes les feuilles
    text_parts = []
    for sheet_name, sheet_df in df.items():
        text_parts.append(f"=== Feuille: {sheet_name} ===")
        text_parts.append(sheet_df.to_string())
    return "\n\n".join(text_parts)


def _extract_text_from_csv(path: Path) -> str:
    """Extrait le texte d'un fichier CSV."""
    if pd is None:
        raise RuntimeError("pandas non installé. Exécutez : pip install pandas")
    df = pd.read_csv(path)
    return df.to_string()


def _extract_text_from_txt(path: Path) -> str:
    """Lit le contenu d'un fichier texte brut."""
    return path.read_text(encoding="utf-8")


def _extract_text_from_file(path: Path) -> str:
    """Détecte le type de fichier et extrait le texte avec la méthode appropriée."""
    suffix = path.suffix.lower()
    
    if suffix == ".pdf":
        return _extract_text_from_pdf(path)
    elif suffix == ".docx":
        return _extract_text_from_docx(path)
    elif suffix in (".txt", ".text"):
        return _extract_text_from_txt(path)
    elif suffix in (".xlsx", ".xls"):
        return _extract_text_from_excel(path)
    elif suffix == ".csv":
        return _extract_text_from_csv(path)
    else:
        # Par défaut, tenter de lire comme texte brut
        try:
            return _extract_text_from_txt(path)
        except Exception:
            raise RuntimeError(f"Type de fichier non supporté : {suffix}")


def extract_document(path: Path) -> ExtractedDocument:
    """Point d'entrée : détecte le type puis extrait via Structured Output.

    1. Lit le texte brut du fichier (PDF, DOCX, TXT, images, CSV, Excel...)
    2. Détecte le type (order / invoice) via LLM
    3. Extrait les champs avec le schéma Pydantic correspondant
    4. Retourne un objet Order ou Invoice validé automatiquement
    """
    text = _extract_text_from_file(path)
    doc_type = detect_document_type(text)

    if doc_type == "invoice":
        invoice = extract_invoice_with_llm(text, Invoice)
        invoice.source_file = str(path)
        return invoice

    order = extract_order_with_llm(text, Order)
    order.source_file = str(path)
    return order

