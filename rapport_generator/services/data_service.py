"""
Service d'ingestion — Lecture et normalisation des données (CSV, JSON, démo)
"""
import csv
import json
import io
from typing import Any


# ── Données de démo ───────────────────────────────────────────────────────────
DEMO_DATA = {
    "financial": {
        "name": "Rapport Financier Q4 2024",
        "type": "financial",
        "data": {
            "revenue": [
                {"month": "Octobre", "value": 842000, "prev_year": 710000},
                {"month": "Novembre", "value": 963000, "prev_year": 780000},
                {"month": "Décembre", "value": 1120000, "prev_year": 890000},
            ],
            "expenses": [
                {"category": "Personnel", "amount": 520000, "pct": 48},
                {"category": "Infrastructure", "amount": 180000, "pct": 17},
                {"category": "Marketing", "amount": 145000, "pct": 13},
                {"category": "R&D", "amount": 215000, "pct": 20},
                {"category": "Divers", "amount": 21000, "pct": 2},
            ],
            "kpis": {
                "total_revenue": 2925000,
                "total_expenses": 1081000,
                "net_profit": 1844000,
                "margin_pct": 63.1,
                "growth_yoy": 22.4,
                "active_clients": 1247,
            },
        },
    },
    "technical": {
        "name": "Rapport Technique Système — Q4 2024",
        "type": "technical",
        "data": {
            "performance": [
                {"metric": "Disponibilité", "value": 99.94, "unit": "%", "sla": 99.9},
                {"metric": "Latence P50", "value": 42, "unit": "ms", "sla": 100},
                {"metric": "Latence P99", "value": 187, "unit": "ms", "sla": 500},
                {"metric": "Throughput", "value": 8420, "unit": "req/s"},
                {"metric": "Taux d'erreur", "value": 0.03, "unit": "%", "sla": 0.1},
                {"metric": "CPU moyen", "value": 34, "unit": "%"},
            ],
            "incidents": [
                {"date": "2024-10-08", "severity": "P2", "duration_min": 43, "description": "Pic connexions DB"},
                {"date": "2024-11-15", "severity": "P3", "duration_min": 12, "description": "Cache miss élevé"},
                {"date": "2024-12-02", "severity": "P1", "duration_min": 8, "description": "Rollback déploiement"},
            ],
            "services": [
                {"name": "API Gateway", "status": "healthy", "uptime": 99.98},
                {"name": "Auth Service", "status": "healthy", "uptime": 99.96},
                {"name": "Data Pipeline", "status": "degraded", "uptime": 98.7},
                {"name": "ML Inference", "status": "healthy", "uptime": 99.91},
                {"name": "Storage", "status": "healthy", "uptime": 100.0},
            ],
        },
    },
    "medical": {
        "name": "Rapport Médical — Étude COHORTE-24",
        "type": "medical",
        "data": {
            "demographics": {
                "total_participants": 342,
                "mean_age": 54.2,
                "std_age": 8.3,
                "female_pct": 58,
                "male_pct": 42,
                "dropout_rate": 4.1,
            },
            "treatment_outcomes": [
                {"group": "Traitement A", "n": 114, "success": 87, "adverse_events": 8, "dropout": 5},
                {"group": "Traitement B", "n": 115, "success": 79, "adverse_events": 14, "dropout": 7},
                {"group": "Contrôle", "n": 113, "success": 61, "adverse_events": 6, "dropout": 2},
            ],
            "biomarkers": [
                {"name": "CRP", "baseline": 18.4, "followup_6m": 7.2, "unit": "mg/L", "p_value": 0.001},
                {"name": "IL-6", "baseline": 42.1, "followup_6m": 18.3, "unit": "pg/mL", "p_value": 0.002},
                {"name": "HbA1c", "baseline": 7.8, "followup_6m": 6.9, "unit": "%", "p_value": 0.008},
                {"name": "LDL", "baseline": 145, "followup_6m": 112, "unit": "mg/dL", "p_value": 0.015},
            ],
        },
    },
}


def parse_csv(content: str) -> dict:
    """Parse un fichier CSV et retourne les données structurées."""
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    if not rows:
        raise ValueError("CSV vide ou invalide")

    # Convertir les valeurs numériques automatiquement
    parsed_rows = []
    for row in rows:
        parsed_row = {}
        for k, v in row.items():
            try:
                parsed_row[k] = float(v) if "." in v else int(v)
            except (ValueError, TypeError):
                parsed_row[k] = v
        parsed_rows.append(parsed_row)

    return {
        "rows": parsed_rows,
        "columns": list(rows[0].keys()),
        "row_count": len(parsed_rows),
    }


def parse_json(content: str) -> dict:
    """Parse et valide un JSON."""
    try:
        data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")


def detect_report_type(data: dict) -> str:
    """Détecte automatiquement le type de rapport depuis les données."""
    data_str = json.dumps(data).lower()

    financial_keywords = ["revenue", "expense", "profit", "margin", "cost", "budget", "chiffre", "bilan"]
    technical_keywords = ["latency", "uptime", "incident", "throughput", "cpu", "memory", "performance", "latence"]
    medical_keywords = ["patient", "treatment", "biomarker", "clinical", "symptom", "medication", "traitement", "cohorte"]

    scores = {
        "financial": sum(1 for k in financial_keywords if k in data_str),
        "technical": sum(1 for k in technical_keywords if k in data_str),
        "medical": sum(1 for k in medical_keywords if k in data_str),
    }

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "generic"


def get_demo_data(report_type: str) -> dict:
    """Retourne les données de démo pour un type donné."""
    return DEMO_DATA.get(report_type, DEMO_DATA["financial"])


def normalize_uploaded_data(raw_data: Any, filename: str = "") -> dict:
    """Normalise les données uploadées en format standard."""
    if isinstance(raw_data, dict):
        # Déjà structuré — vérifier si format attendu
        if "data" in raw_data and "type" in raw_data:
            return raw_data  # Format natif
        # Wrapper dans format standard
        detected_type = detect_report_type(raw_data)
        return {
            "name": raw_data.get("name", filename or "Rapport sans titre"),
            "type": raw_data.get("type", detected_type),
            "data": raw_data,
        }
    elif isinstance(raw_data, list):
        return {
            "name": filename or "Rapport sans titre",
            "type": detect_report_type({"rows": raw_data}),
            "data": {"rows": raw_data, "row_count": len(raw_data)},
        }
    else:
        return {
            "name": filename or "Rapport sans titre",
            "type": "generic",
            "data": {"raw": str(raw_data)},
        }
