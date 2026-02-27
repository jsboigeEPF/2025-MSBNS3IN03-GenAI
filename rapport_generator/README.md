# D5 — Rédacteur de Rapports IA

Application web complète de génération automatique de rapports professionnels avec IA générative.

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | FastAPI (Python) |
| LLM | OpenAI GPT-4o |
| Mémoire vectorielle | Qdrant |
| Recherche web | SearxNG |
| Export | ReportLab (PDF) |
| Frontend | HTML/CSS/JS + Chart.js |

## Pipeline de génération

```
Données (CSV/JSON/Texte/Démo)
  → SearxNG (enrichissement web temps réel)
  → GPT-4o (narratif + KPIs + Charts config)
  → Rapport affiché (narratif + graphiques)
  → Qdrant (sauvegarde vectorielle)
  → PDF téléchargeable (ReportLab)
```

## Installation

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

L'app sera disponible sur http://localhost:8000

## Structure du projet

```
rapport_generator/
├── main.py                  # Point d'entrée FastAPI
├── config.py                # Configuration (clés API)
├── requirements.txt
├── routes/
│   ├── reports.py           # API génération rapports
│   ├── data.py              # API ingestion données
│   └── export.py            # API export PDF
├── services/
│   ├── openai_service.py    # GPT-4o (narratif, KPIs, charts)
│   ├── qdrant_service.py    # Mémoire vectorielle
│   ├── searxng_service.py   # Enrichissement web
│   ├── pdf_service.py       # Génération PDF ReportLab
│   └── data_service.py      # Parsing CSV/JSON/démo
├── templates/
│   └── index.html           # Frontend principal
├── static/
│   ├── css/style.css
│   └── js/app.js
└── exports/                 # PDFs générés (auto-créé)
```

## Types de rapports supportés

- **Financier** : CA, marges, charges, KPIs trimestriels
- **Technique** : Uptime, latences, incidents, services
- **Médical** : Cohortes, biomarqueurs, outcomes cliniques
- **Générique** : Tout type de données (auto-détection)

## Sources de données supportées

- Upload **CSV** (auto-parsing)
- Upload **JSON** (structure libre)
- **Saisie manuelle** JSON
- **Texte brut** (extraction GPT)
- **Données démo** intégrées

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reports/generate` | Génère un rapport complet |
| GET | `/api/reports/demo/{type}` | Données de démo |
| GET | `/api/reports/history` | Historique Qdrant |
| POST | `/api/reports/search` | Recherche sémantique |
| POST | `/api/data/upload` | Upload CSV/JSON |
| POST | `/api/data/extract` | Extraction depuis texte |
| POST | `/api/export/pdf` | Génère un PDF |
| GET | `/api/export/download/{filename}` | Télécharge un PDF |

## Configuration

Toutes les clés API sont dans `config.py`. Pour surcharger, créer un `.env` :

```env
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
SEARXNG_URL=https://...
PORT=8000
```
