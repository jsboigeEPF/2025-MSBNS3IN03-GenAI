"""
Module de pipeline d'analyse de données.

Ce module fournit une fonction de haut niveau pour orchestrer
le pipeline complet: ingest -> clean -> analyze -> viz -> report.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union

import pandas as pd

from src.ingest import load_data
from src.clean import clean_data
from src.analyze import analyze_data
from src.viz import generate_viz
from src.report import generate_report

logger = logging.getLogger(__name__)


def run_pipeline(
    data_path: str,
    config_path: str = "config.yaml",
    outdir: str = "outputs"
) -> Dict[str, Any]:
    """
    Exécute le pipeline complet d'analyse de données.

    Orchestre:
    1. Ingestion des données
    2. Nettoyage
    3. Analyse
    4. Visualisation
    5. Génération de rapports

    Args:
        data_path: Chemin vers le fichier CSV/Excel à analyser
        config_path: Chemin vers le fichier de configuration YAML
        outdir: Répertoire de sortie

    Returns:
        Dict contenant:
        - df_clean: DataFrame nettoyé (ou sample si trop volumineux)
        - ingestion_meta: Métadonnées d'ingestion
        - data_quality_summary: Résumé de qualité des données
        - analysis_summary: Résumé d'analyse complet
        - insights: Liste d'insights générés
        - figures: Dictionnaire des visualisations {type: [paths]}
        - report_path: Chemin vers le rapport Markdown généré
    """
    data_path = Path(data_path)
    config_path = Path(config_path)
    outdir = Path(outdir)

    # Créer les répertoires de sortie
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "figures").mkdir(parents=True, exist_ok=True)

    # Charger la configuration
    config = {}
    if config_path.exists():
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    results = {}

    # Étape 1: Ingestion
    logger.info("=" * 50)
    logger.info("ÉTAPE 1: Ingestion des données")
    logger.info("=" * 50)

    try:
        df, ingestion_meta = load_data(
            data_path,
            encoding=config.get("data", {}).get("encoding"),
            separator=config.get("data", {}).get("separator"),
            skiprows=config.get("data", {}).get("skip_rows", 0)
        )
        results["ingestion_meta"] = ingestion_meta
        logger.info(f"Données ingestées: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    except Exception as e:
        logger.error(f"Erreur d'ingestion: {e}")
        raise

    # Étape 2: Nettoyage
    logger.info("=" * 50)
    logger.info("ÉTAPE 2: Nettoyage des données")
    logger.info("=" * 50)

    cleaning_config = config.get("cleaning", {})
    try:
        df_clean, data_quality_summary = clean_data(
            df,
            handle_duplicates=cleaning_config.get("handle_duplicates", True),
            handle_outliers=cleaning_config.get("handle_outliers", True),
            winsorize=cleaning_config.get("winsorize", False),
            normalize_strings=cleaning_config.get("normalize_strings", True),
            infer_types=cleaning_config.get("infer_types", True)
        )

        # Sauvegarder les données nettoyées
        cleaned_path = outdir / "cleaned.csv"
        df_clean.to_csv(cleaned_path, index=False)
        logger.info(f"Données nettoyées sauvegardées: {cleaned_path}")

        results["df_clean"] = df_clean
        results["data_quality_summary"] = data_quality_summary
        logger.info(f"Données nettoyées: {df_clean.shape[0]} lignes")
    except Exception as e:
        logger.error(f"Erreur de nettoyage: {e}")
        df_clean = df
        data_quality_summary = {}
        results["df_clean"] = df_clean
        results["data_quality_summary"] = {"error": str(e)}

    # Étape 3: Analyse
    logger.info("=" * 50)
    logger.info("ÉTAPE 3: Analyse des données")
    logger.info("=" * 50)

    try:
        analysis_summary, insights, viz_suggestions = analyze_data(
            df_clean,
            llm_config=config.get("llm")
        )
        results["analysis_summary"] = analysis_summary
        results["insights"] = insights
        results["viz_suggestions"] = viz_suggestions
        logger.info(f"Analyse complétée: {len(insights)} insights, {len(viz_suggestions)} suggestions")
    except Exception as e:
        logger.error(f"Erreur d'analyse: {e}")
        analysis_summary = {}
        insights = []
        viz_suggestions = []
        results["analysis_summary"] = {"error": str(e)}
        results["insights"] = []
        results["viz_suggestions"] = []

    # Étape 4: Visualisation
    logger.info("=" * 50)
    logger.info("ÉTAPE 4: Génération de visualisations")
    logger.info("=" * 50)

    try:
        figures = generate_viz(
            df_clean,
            output_dir=outdir,
            viz_suggestions=viz_suggestions,
            prefix="analysis"
        )
        results["figures"] = figures
        total_viz = sum(len(v) for v in figures.values())
        logger.info(f"Visualisations générées: {total_viz} fichiers")
    except Exception as e:
        logger.error(f"Erreur de visualisation: {e}")
        figures = {}
        results["figures"] = {"error": str(e)}

    # Étape 5: Rapport
    logger.info("=" * 50)
    logger.info("ÉTAPE 5: Génération du rapport")
    logger.info("=" * 50)

    try:
        report_path = generate_report(
            analysis_summary=analysis_summary,
            figures_dir=outdir / "figures",
            llm_config=config.get("llm")
        )
        results["report_path"] = str(report_path)
        logger.info(f"Rapport généré: {report_path}")
    except Exception as e:
        logger.error(f"Erreur de génération de rapport: {e}")
        results["report_path"] = None

    # Sauvegarder summary.json
    logger.info("=" * 50)
    logger.info("Sauvegarde du résumé complet")
    logger.info("=" * 50)

    try:
        # Préparer le résumé sérialisable
        summary = {
            "metadata": {
                "input_file": str(data_path),
                "output_dir": str(outdir),
                "timestamp": str(pd.Timestamp.now().isoformat())
            },
            "ingestion_meta": results.get("ingestion_meta", {}),
            "data_quality_summary": results.get("data_quality_summary", {}),
            "analysis_summary": results.get("analysis_summary", {}),
            "figures": results.get("figures", {}),
            "insights": results.get("insights", []),
            "viz_suggestions": results.get("viz_suggestions", [])
        }

        # Custom encoder pour les types non JSON sérialisables
        def json_serializer(obj):
            if isinstance(obj, Path):
                return str(obj)
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            elif isinstance(obj, (pd.Timestamp, pd.Period)):
                return str(obj)
            elif isinstance(obj, (pd.Series, pd.DataFrame)):
                return obj.to_dict()
            elif hasattr(obj, '__dict__'):
                return str(obj)
            return str(obj)

        summary_path = outdir / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=json_serializer)
        logger.info(f"Résumé complet sauvegardé: {summary_path}")

    except Exception as e:
        logger.error(f"Erreur sauvegarde summary.json: {e}")

    # Sauvegarder les métadonnées d'exécution
    try:
        execution_meta = {
            "input_file": str(data_path),
            "config_used": str(config_path),
            "output_dir": str(outdir),
            "results_summary": {}
        }
        for k, v in results.items():
            # Les listes sont toujours un succès (même si vides)
            if isinstance(v, list):
                execution_meta["results_summary"][k] = {"success": True, "error": None, "count": len(v)}
            elif isinstance(v, dict):
                execution_meta["results_summary"][k] = {"success": v.get("error") is None, "error": v.get("error", None)}
            else:
                execution_meta["results_summary"][k] = {"success": True, "error": None}
        results_file = outdir / "execution_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(execution_meta, f, indent=2, default=str)
        logger.info(f"Métadonnées sauvegardées: {results_file}")
    except Exception as e:
        logger.error(f"Erreur sauvegarde execution_results.json: {e}")

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module de pipeline chargé.")
    print("Utilisez run_pipeline(data_path, config_path, outdir)")
