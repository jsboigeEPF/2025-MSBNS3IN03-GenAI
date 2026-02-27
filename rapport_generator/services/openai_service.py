"""
Service OpenAI — Génération de narratifs IA et analyse de données
"""
import json
from openai import AsyncOpenAI
from config import settings
from typing import Any


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Prompts par type de rapport
SYSTEM_PROMPTS = {
    "financial": """Tu es un analyste financier senior avec 15 ans d'expérience. 
Tu rédiges des rapports financiers professionnels en français, précis, concis et actionnables.
Utilise la terminologie financière appropriée. Structure tes analyses avec des insights clairs.
Formate en Markdown : **gras** pour les points clés, ## pour les sections.""",

    "technical": """Tu es un ingénieur DevOps / architecte système expert.
Tu rédiges des rapports techniques professionnels en français sur les performances systèmes.
Utilise la terminologie technique appropriée (SLA, MTTR, SLO, latence, throughput).
Sois précis dans les recommandations. Formate en Markdown.""",

    "medical": """Tu es un biostatisticien et rédacteur médical certifié.
Tu rédiges des rapports d'études cliniques en français, rigoureux et conformes aux standards ICH/GCP.
Mentionne les significativités statistiques, intervalles de confiance, et conclusions basées sur les preuves.
Formate en Markdown. Reste objectif et factuel.""",

    "generic": """Tu es un expert en analyse de données et rédaction professionnelle.
Tu génères des rapports structurés en français à partir de données brutes.
Identifie les tendances, anomalies et points d'action. Formate en Markdown.""",
}


async def generate_narrative(
    report_type: str,
    data: dict[str, Any],
    report_name: str,
    search_context: str = "",
    extra_instructions: str = "",
) -> str:
    """Génère un narratif analytique complet via GPT-4o."""

    system = SYSTEM_PROMPTS.get(report_type, SYSTEM_PROMPTS["generic"])

    context_section = ""
    if search_context:
        context_section = f"""
## Contexte marché actuel (source: recherche web)
{search_context}

---
"""

    user_prompt = f"""Génère un rapport analytique complet pour : **{report_name}**

{context_section}## Données à analyser
```json
{json.dumps(data, ensure_ascii=False, indent=2)}
```

## Instructions
- Rédigez un rapport de 4-5 paragraphes denses (400-550 mots)
- Section 1 : **Synthèse exécutive** — chiffres clés et tendance générale
- Section 2 : **Analyse détaillée** — décortiquer les données importantes
- Section 3 : **Points d'attention** — risques, anomalies, écarts
- Section 4 : **Recommandations** — 3-5 actions concrètes et prioritisées
- Utilise **gras** pour les métriques importantes
- Ajoute des pourcentages et comparaisons chiffrées quand possible
{extra_instructions}"""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1200,
    )

    return response.choices[0].message.content


async def extract_structured_data(raw_text: str, report_type: str) -> dict:
    """Extrait des données structurées depuis du texte brut (CSV mal formaté, notes, etc.)."""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_MINI,
        messages=[
            {
                "role": "system",
                "content": "Tu extrais des données structurées depuis du texte brut. Réponds UNIQUEMENT en JSON valide, sans markdown."
            },
            {
                "role": "user",
                "content": f"""Extrait les données de ce texte de type '{report_type}' en JSON structuré.
Retourne un objet JSON avec les clés pertinentes pour ce type de rapport.

Texte:
{raw_text}"""
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


async def generate_kpi_summary(data: dict, report_type: str) -> dict:
    """Génère un résumé des KPIs clés sous forme structurée (pour les cartes)."""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_MINI,
        messages=[
            {
                "role": "system",
                "content": "Tu extrais les KPIs principaux. Réponds UNIQUEMENT en JSON valide, sans markdown ni backticks."
            },
            {
                "role": "user",
                "content": f"""Pour ce rapport de type '{report_type}', extrait exactement 4 KPIs principaux.

Données: {json.dumps(data, ensure_ascii=False)}

Retourne ce JSON exact:
{{
  "kpis": [
    {{"label": "Nom du KPI", "value": "Valeur avec unité", "trend": "+X% ou -X% ou neutre", "color": "green|red|blue|gold"}},
    ...4 items total
  ]
}}"""
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


async def generate_chart_config(data: dict, report_type: str) -> list[dict]:
    """Génère les configurations Chart.js pour visualiser les données."""

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL_MINI,
        messages=[
            {
                "role": "system",
                "content": "Tu génères des configurations Chart.js. Réponds UNIQUEMENT en JSON valide."
            },
            {
                "role": "user",
                "content": f"""Génère 2 configurations Chart.js pour visualiser ces données de type '{report_type}'.

Données: {json.dumps(data, ensure_ascii=False)}

Retourne ce JSON:
{{
  "charts": [
    {{
      "id": "chart1",
      "title": "Titre du graphique",
      "type": "bar|line|doughnut|radar",
      "data": {{
        "labels": [...],
        "datasets": [{{
          "label": "...",
          "data": [...],
          "backgroundColor": [...],
          "borderColor": "..."
        }}]
      }},
      "options": {{
        "responsive": true,
        "plugins": {{"legend": {{"position": "top"}}, "title": {{"display": true, "text": "..."}}}}
      }}
    }}
  ]
}}"""
            }
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("charts", [])
