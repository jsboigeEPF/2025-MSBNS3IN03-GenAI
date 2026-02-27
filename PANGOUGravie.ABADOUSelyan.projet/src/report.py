"""
Module de génération de rapports (Report).

Ce module fournit des fonctions pour générer des rapports Markdown
à partir des résultats d'analyse de données.
"""
from datetime import datetime
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

from src.config_env import is_llm_enabled as llm_enabled
from src.llm import run_llm_text, LLMError

logger = logging.getLogger(__name__)

# Répertoire par défaut pour les rapports
DEFAULT_REPORTS_DIR = "outputs"


def format_number(value: float, decimals: int = 2) -> str:
    """Formater un nombre avec des séparateurs de milliers."""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        if abs(value) < 1 and value != 0:
            return f"{value:.{decimals}f}"
        return f"{value:,.{decimals}f}".replace(",", " ")
    except (ValueError, TypeError):
        return str(value)


def format_percentage(value: float, decimals: int = 1) -> str:
    """Formater un nombre en pourcentage."""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        return f"{value:.{decimals}f}%"
    except (ValueError, TypeError):
        return str(value)


def generate_overview(
    analysis_summary: Dict[str, Any],
    llm_config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Génère la section Overview du rapport.

    Args:
        analysis_summary: Résultats de l'analyse
        llm_config: Configuration LLM

    Returns:
        str: Section overview en Markdown
    """
    shape = analysis_summary.get("shape", {})
    rows = shape.get("rows", 0)
    cols = shape.get("columns", 0)
    memory_bytes = analysis_summary.get("memory_bytes", 0)

    # Formater la mémoire
    if memory_bytes > 1024 * 1024:
        memory_str = f"{memory_bytes / (1024 * 1024):.2f} MB"
    elif memory_bytes > 1024:
        memory_str = f"{memory_bytes / 1024:.2f} KB"
    else:
        memory_str = f"{memory_bytes} bytes"

    # Détecter les types de colonnes
    column_types = analysis_summary.get("column_types", {})
    numeric_count = sum(1 for t in column_types.values() if t.get("type") == "numeric")
    categorical_count = sum(1 for t in column_types.values() if t.get("type") == "categorical")
    datetime_count = sum(1 for t in column_types.values() if t.get("type") == "datetime")

    overview = f"""# Aperçu du Dataset

## Informations Générales

| Métrique | Valeur |
|----------|--------|
| Nombre de lignes | {format_number(rows)} |
| Nombre de colonnes | {format_number(cols)} |
| Taille mémoire | {memory_str} |
| Données manquantes totales | {format_number(analysis_summary.get('missingness', {}).get('total_na', 0))} |
| Pourcentage de valeurs manquantes | {format_percentage(analysis_summary.get('missingness', {}).get('percentage_na', 0))} |

## Répartition des Colonnes

- **Numériques**: {format_number(numeric_count)} colonnes
- **Catégorielles**: {format_number(categorical_count)} colonnes
- **Date/Heure**: {format_number(datetime_count)} colonnes

---

"""
    return overview


def generate_executive_summary(
    analysis_summary: Dict[str, Any],
    insights: List[Dict[str, Any]],
    llm_config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Génère un résumé exécutif avec LLM.

    Args:
        analysis_summary: Résultats de l'analyse
        insights: Liste des insights
        llm_config: Configuration LLM

    Returns:
        str: Résumé exécutif en Markdown
    """
    # Vérifier si LLM est activé
    if not llm_enabled(llm_config):
        # Fallback: résumé basique
        return """## Résumé Exécutif

Ce rapport présente une analyse complète du dataset. Les insights clés identifiés sont :

- Le dataset contient {rows} lignes et {cols} colonnes
- {missing_pct}% des valeurs sont manquantes
- {insight_count} insights ont été générés
- {viz_suggestions_count} visualisations sont recommandées

Pour plus de détails, veuillez consulter les sections suivantes.
""".format(
            rows=analysis_summary.get("shape", {}).get("rows", 0),
            cols=analysis_summary.get("shape", {}).get("columns", 0),
            missing_pct=format_percentage(analysis_summary.get("missingness", {}).get("percentage_na", 0)),
            insight_count=len(insights),
            viz_suggestions_count=len(analysis_summary.get("viz_suggestions", []))
        )

    try:
        # Préparer le contexte compact pour LLM
        context = f"""
Dataset: {analysis_summary['shape']['rows']} lignes, {analysis_summary['shape']['columns']} colonnes
Types de colonnes: {analysis_summary['column_types']}

Insights générés ({len(insights)}):
{insights[:5] if len(insights) > 5 else insights}

Corrélations fortes:
{analysis_summary.get('correlations', {}).get('strong_correlations', [])}
"""

        system_prompt = """Tu es un analyste de données expert. Rédige un résumé exécutif concis (5-8 lignes) à partir des informations suivantes.

Instructions:
- Sois concis et direct
- Mets en avant les points les plus importants
- Utilise des phrases complètes
- Évite les détails techniques
- Reste neutre et factuel
"""

        try:
            summary = run_llm_text(
                llm_config or {"llm": {"enabled": True, "model": "gpt-4o"}},
                system_prompt,
                context
            )
            return f"## Résumé Exécutif\n\n{summary.strip()}\n\n---\n"
        except Exception as e:
            logger.warning(f"Erreur LLM pour executive summary: {e}")
            # Fallback
            return generate_executive_summary(analysis_summary, insights, None)

    except Exception as e:
        logger.warning(f"Erreur génération executive summary: {e}")
        return """## Résumé Exécutif

Analyse complète du dataset effectuée. Consultez les sections ci-dessous pour plus de détails.

---
"""


def generate_data_quality_summary(
    analysis_summary: Dict[str, Any],
    missing_values: Optional[Dict[str, Any]] = None
) -> str:
    """
    Génère la section Data Quality Summary.

    Args:
        analysis_summary: Résultats de l'analyse
        missing_values: Résumé des valeurs manquantes

    Returns:
        str: Section data quality en Markdown
    """
    missingness = analysis_summary.get("missingness", {})
    missing_pct = missingness.get("percentage_na", 0)

    quality_score = 100 - missing_pct
    if quality_score >= 95:
        quality_level = "Excellent"
        quality_emoji = "✅"
    elif quality_score >= 80:
        quality_level = "Bon"
        quality_emoji = "⚠️"
    elif quality_score >= 60:
        quality_level = "Moyen"
        quality_emoji = "⚠️"
    else:
        quality_level = "Faible"
        quality_emoji = "❌"

    columns_info = analysis_summary.get("column_types", {})

    # Colonnes avec plus de 10% de NA
    cols_with_na = []
    for col, info in columns_info.items():
        na_pct = info.get("missing_pct", 0)
        if na_pct > 10:
            cols_with_na.append((col, na_pct))

    # Colonnes avec plus de 25% de NA
    critical_cols = [(col, pct) for col, pct in cols_with_na if pct > 25]

    quality_section = f"""# Qualité des Données

## Score de Qualité: {quality_emoji} {quality_score:.1f}% ({quality_level})

| Métrique | Valeur |
|----------|--------|
| Total de valeurs manquantes | {format_number(missingness.get('total_na', 0))} |
| Pourcentage de valeurs manquantes | {format_percentage(missing_pct)} |
| Duplicates détectés | {format_number(analysis_summary.get('duplicates', 0))} |

## Colonnes avec des Problèmes de Qualité

### Colonnes avec plus de 10% de valeurs manquantes ({len(cols_with_na)} colonnes)
"""
    if cols_with_na:
        quality_section += "| Colonnes | % Manquant |\n"
        quality_section += "|----------|------------|\n"
        for col, pct in sorted(cols_with_na, key=lambda x: -x[1]):
            quality_section += f"| {col} | {format_percentage(pct)} |\n"
    else:
        quality_section += "*Aucune colonne avec plus de 10% de valeurs manquantes.*\n"

    if critical_cols:
        quality_section += "\n### Colonnes critiques (plus de 25% de valeurs manquantes)\n"
        quality_section += "| Colonnes | % Manquant | Recommandation |\n"
        quality_section += "|----------|------------|----------------|\n"
        for col, pct in sorted(critical_cols, key=lambda x: -x[1]):
            quality_section += f"| {col} | {format_percentage(pct)} | Considérer la suppression ou imputation avancée |\n"

    # Vérifier les high cardinality
    cardinalities = analysis_summary.get("cardinalities", {})
    high_card_cols = [
        (col, info) for col, info in cardinalities.items()
        if info.get("unique_pct", 0) > 90
    ]

    if high_card_cols:
        quality_section += "\n### Colonnes à forte cardinalité\n"
        quality_section += "*Ces colonnes ont plus de 90% de valeurs uniques.*\n\n"
        quality_section += "| Colonnes | Valeurs uniques | % |\n"
        quality_section += "|----------|-----------------|---|\n"
        for col, info in high_card_cols[:5]:
            quality_section += f"| {col} | {format_number(info.get('unique_count', 0))} | {format_percentage(info.get('unique_pct', 0))} |\n"

    quality_section += "\n---\n"
    return quality_section


def generate_key_statistics(
    analysis_summary: Dict[str, Any]
) -> str:
    """
    Génère la section Key Statistics.

    Args:
        analysis_summary: Résultats de l'analyse

    Returns:
        str: Section key statistics en Markdown
    """
    statistics_section = "# Statistiques Clés\n\n"

    # Statistiques numériques
    numeric_stats = analysis_summary.get("numeric_stats", {})
    if numeric_stats:
        statistics_section += "## Statistiques Numériques\n\n"
        statistics_section += "| Colonnes | Moyenne | Médiane | Écart-type | Min | Max |\n"
        statistics_section += "|----------|---------|---------|------------|-----|-----|\n"
        for col, stats in list(numeric_stats.items())[:10]:  # Top 10
            mean = stats.get("mean")
            median = stats.get("median")
            std = stats.get("std")
            min_val = stats.get("min")
            max_val = stats.get("max")
            statistics_section += f"| {col} | {format_number(mean)} | {format_number(median)} | {format_number(std)} | {format_number(min_val)} | {format_number(max_val)} |\n"

    # Statistiques catégorielles
    categorical_stats = analysis_summary.get("categorical_stats", {})
    if categorical_stats:
        statistics_section += "\n## Statistiques Catégorielles\n\n"
        statistics_section += "| Colonnes | Valeurs uniques | Mode | Fréquence Mode |\n"
        statistics_section += "|----------|-----------------|------|----------------|\n"
        for col, stats in list(categorical_stats.items())[:10]:  # Top 10
            unique_count = stats.get("unique_count", 0)
            most_frequent = stats.get("most_frequent", {})
            mode = most_frequent.get("value", "N/A")
            mode_count = most_frequent.get("count", 0)
            statistics_section += f"| {col} | {format_number(unique_count)} | {mode} | {format_number(mode_count)} |\n"

    # Analyse des dates
    date_stats = analysis_summary.get("date_stats", {})
    if date_stats:
        statistics_section += "\n## Analyse des Dates\n\n"
        statistics_section += "| Colonnes | Période | Écart (jours) | Échantillon |\n"
        statistics_section += "|----------|---------|---------------|-------------|\n"
        for col, stats in date_stats.items():
            min_date = stats.get("min", "N/A")
            max_date = stats.get("max", "N/A")
            range_days = stats.get("range_days", "N/A")
            sample = stats.get("sample_values", [])[:1]
            statistics_section += f"| {col} | {min_date} à {max_date} | {format_number(range_days)} | {sample[0] if sample else 'N/A'} |\n"

    # Corrélations
    correlations = analysis_summary.get("correlations", {}).get("strong_correlations", [])
    if correlations:
        statistics_section += "\n## Corrélations Fortes\n\n"
        statistics_section += "| Colonne 1 | Colonne 2 | Corrélation | Force |\n"
        statistics_section += "|-----------|-----------|-------------|--------|\n"
        for corr in correlations[:10]:  # Top 10
            col1 = corr.get("col1", "N/A")
            col2 = corr.get("col2", "N/A")
            correlation = corr.get("correlation", 0)
            strength = corr.get("strength", "unknown")
            statistics_section += f"| {col1} | {col2} | {format_number(correlation)} | {strength} |\n"

    statistics_section += "\n---\n"
    return statistics_section


def generate_visualizations(
    figures_dir: Path,
    viz_suggestions: List[Dict[str, Any]]
) -> str:
    """
    Génère la section Visualizations avec liens vers les PNG.

    Args:
        figures_dir: Répertoire contenant les figures
        viz_suggestions: Liste des suggestions de visualisation

    Returns:
        str: Section visualizations en Markdown
    """
    visualizations_section = "# Visualisations\n\n"

    if not figures_dir.exists():
        visualizations_section += "*Aucune visualisation générée.*\n\n---\n"
        return visualizations_section

    # Lister les fichiers PNG
    png_files = sorted(figures_dir.glob("*.png"))

    # Grouper par type
    viz_types = {
        "histograms": [],
        "boxplots": [],
        "barcharts": [],
        "scatterplots": [],
        "timeseries": [],
        "heatmaps": [],
        "custom": []
    }

    for png_file in png_files:
        filename = png_file.name
        if "hist" in filename.lower():
            viz_types["histograms"].append(png_file)
        elif "box" in filename.lower():
            viz_types["boxplots"].append(png_file)
        elif "bar" in filename.lower():
            viz_types["barcharts"].append(png_file)
        elif "scatter" in filename.lower():
            viz_types["scatterplots"].append(png_file)
        elif "ts" in filename.lower() or "timeseries" in filename.lower():
            viz_types["timeseries"].append(png_file)
        elif "corr_heatmap" in filename.lower() or "heatmap" in filename.lower():
            viz_types["heatmaps"].append(png_file)
        else:
            viz_types["custom"].append(png_file)

    # Créer les sections pour chaque type
    type_labels = {
        "histograms": "Histogrammes",
        "boxplots": "Boxplots",
        "barcharts": "Bar Charts",
        "scatterplots": "Scatter Plots",
        "timeseries": "Séries Temporelles",
        "heatmaps": "Heatmaps de Corrélation",
        "custom": "Visualisations Personnalisées"
    }

    for viz_type, files in viz_types.items():
        if files:
            visualizations_section += f"## {type_labels.get(viz_type, viz_type)}\n\n"
            for png_file in files:
                rel_path = png_file.relative_to(figures_dir.parent)
                visualizations_section += f"![{png_file.stem}]({rel_path})\n\n"
            visualizations_section += "\n"

    # Ajouter les suggestions de visualisation
    if viz_suggestions:
        visualizations_section += "## Suggestions de Visualisation\n\n"
        visualizations_section += "| Type | Colonnes | Objectif |\n"
        visualizations_section += "|------|----------|----------|\n"
        for suggestion in viz_suggestions[:10]:
            viz_type = suggestion.get("type", "unknown")
            columns = suggestion.get("columns", []) or [suggestion.get("column", "N/A")]
            purpose = suggestion.get("purpose", suggestion.get("description", "N/A"))
            visualizations_section += f"| {viz_type} | {', '.join(map(str, columns))} | {purpose} |\n"
        visualizations_section += "\n---\n"

    return visualizations_section


def generate_insights(
    insights: List[Dict[str, Any]],
    hypotheses: List[Dict[str, Any]]
) -> str:
    """
    Génère la section Insights.

    Args:
        insights: Liste des insights
        hypotheses: Liste des hypothèses

    Returns:
        str: Section insights en Markdown
    """
    insights_section = "# Insights et Hypothèses\n\n"

    # Insights (>= 8)
    if insights:
        insights_section += "## Insights Clés\n\n"
        for i, insight in enumerate(insights[:15], 1):  # Jusqu'à 15 insights
            title = insight.get("title", "Sans titre")
            description = insight.get("description", insight.get("text", ""))
            severity = insight.get("severity", "info")
            impact = insight.get("impact", "medium")

            # Emoji selon la sévérité
            if severity == "high":
                emoji = "🔴"
            elif severity == "medium":
                emoji = "🟡"
            else:
                emoji = "🔵"

            insights_section += f"{emoji} **{i}. {title}**\n\n{description}\n\n"

            # Recommendation si présente
            recommendation = insight.get("recommendation", "")
            if recommendation:
                insights_section += f"*Recommandation: {recommendation}*\n\n"

    else:
        insights_section += "*Aucun insight généré.*\n\n"

    # Hypothèses
    if hypotheses:
        insights_section += "## Hypothèses à Explorer\n\n"
        for i, hypothesis in enumerate(hypotheses[:10], 1):
            title = hypothesis.get("title", "Sans titre")
            description = hypothesis.get("description", hypothesis.get("text", ""))
            validation = hypothesis.get("validation", "")

            insights_section += f"**{i}. {title}**\n\n{description}\n\n"
            if validation:
                insights_section += f"*Validation: {validation}*\n\n"

    insights_section += "---\n"
    return insights_section


def generate_next_steps(
    insights: List[Dict[str, Any]],
    viz_suggestions: List[Dict[str, Any]],
    analysis_summary: Dict[str, Any]
) -> str:
    """
    Génère la section Next Steps.

    Args:
        insights: Liste des insights
        viz_suggestions: Liste des suggestions de visualisation
        analysis_summary: Résumé de l'analyse

    Returns:
        str: Section next steps en Markdown
    """
    next_steps_section = "# Prochaines Étapes\n\n"

    # Extraire des recommandations basées sur les insights
    recommendations = []

    # Si données manquantes
    missing_pct = analysis_summary.get("missingness", {}).get("percentage_na", 0)
    if missing_pct > 10:
        recommendations.append("1. **Traitement des valeurs manquantes** : Une analyse plus poussée des pattern de missing est recommandée.")

    # Si outliers détectés
    outliers_detected = analysis_summary.get("outliers_detected", {})
    if outliers_detected:
        outlier_cols = [col for col, stats in outliers_detected.items() if stats.get("count", 0) > 0]
        if outlier_cols:
            recommendations.append(f"2. **Analyse des outliers** : {len(outlier_cols)} colonnes contiennent des outliers. Investigation recommandée.")

    # Si corrélations fortes
    strong_correlations = analysis_summary.get("correlations", {}).get("strong_correlations", [])
    if strong_correlations:
        recommendations.append("3. **Exploration des corrélations** : Plusieurs paires de variables fortement corrélées ont été détectées. Analyser les relations causales.")

    # Si insights disponibles
    if insights:
        high_severity = [i for i in insights if i.get("severity") == "high"]
        if high_severity:
            recommendations.append(f"4. **Actions prioritaires** : {len(high_severity)} insights de haute sévérité nécessitent une attention immédiate.")

    # Si visualisations disponibles
    if viz_suggestions:
        recommendations.append(f"5. **Générer les visualisations** : {len(viz_suggestions)} visualisations suggérées peuvent être générées pour approfondir l'analyse.")

    # Recommendations par défaut
    if not recommendations:
        recommendations = [
            "1. **Collecter plus de données** : Des jeux de données plus complets permettraient des analyses plus robustes.",
            "2. **Explorer les relations** : Analyser les corrélations entre les variables numériques.",
            "3. **Segmenter l'analyse** : Découper l'analyse par catégories pour identifier des patterns spécifiques."
        ]

    next_steps_section += "Voici les recommandations pour les prochaines étapes de l'analyse :\n\n"
    for rec in recommendations:
        next_steps_section += f"{rec}\n\n"

    # Plan d'action
    next_steps_section += "## Plan d'Action Recommandé\n\n"
    next_steps_section += "| Étape | Action | Priorité |\n"
    next_steps_section += "|-------|--------|----------|\n"
    next_steps_section += "| 1 | Vérification de la qualité des données | Haute |\n"
    next_steps_section += "| 2 | Exploration des corrélations | Moyenne |\n"
    next_steps_section += "| 3 | Génération de visualisations approfondies | Moyenne |\n"
    next_steps_section += "| 4 | Test d'hypothèses | Haute |\n"

    next_steps_section += "\n---\n"
    return next_steps_section


def generate_report(
    analysis_summary: Dict[str, Any],
    figures_dir: Optional[Union[str, Path]] = None,
    llm_config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Génère un rapport Markdown complet à partir de l'analyse.

    Args:
        analysis_summary: Résultats de l'analyse (de analyze.py)
        figures_dir: Répertoire contenant les figures (outputs/figures/)
        llm_config: Configuration LLM

    Returns:
        str: Chemin vers le fichier report.md généré
    """
    # Résoudre les chemins
    output_dir = Path(DEFAULT_REPORTS_DIR)
    figures_dir = Path(figures_dir) if figures_dir else output_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Récupérer les données
    insights = analysis_summary.get("insights", [])
    hypotheses = analysis_summary.get("hypotheses", [])
    viz_suggestions = analysis_summary.get("viz_suggestions", [])

    # Générer les sections
    sections = []

    # Overview
    sections.append(generate_overview(analysis_summary, llm_config))

    # Executive Summary (si LLM activé)
    if llm_enabled(llm_config):
        try:
            sections.append(generate_executive_summary(analysis_summary, insights, llm_config))
        except Exception as e:
            logger.warning(f"Erreur génération executive summary: {e}")
            sections.append(generate_executive_summary(analysis_summary, insights, None))

    # Data Quality Summary
    missing_values = analysis_summary.get("missing_values", {})
    sections.append(generate_data_quality_summary(analysis_summary, missing_values))

    # Key Statistics
    sections.append(generate_key_statistics(analysis_summary))

    # Visualizations
    sections.append(generate_visualizations(figures_dir, viz_suggestions))

    # Insights
    sections.append(generate_insights(insights, hypotheses))

    # Next Steps
    sections.append(generate_next_steps(insights, viz_suggestions, analysis_summary))

    # Assembler le rapport
    report_content = "# Rapport d'Analyse de Données\n\n"
    report_content += f"*Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    report_content += "---\n\n"
    report_content += "".join(sections)

    # Écrire le fichier
    report_path = output_dir / "report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    logger.info(f"Rapport généré: {report_path}")
    return str(report_path)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module de génération de rapports chargé.")
    print("Utilisez generate_report(analysis_summary) pour générer un rapport.")
