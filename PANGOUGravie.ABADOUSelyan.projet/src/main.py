"""
Point d'entrée principal du Data Analyst Agent.

Ce module orchestre la pipeline complète d'analyse de données:
1. Ingestion des données
2. Nettoyage
3. Analyse
4. Visualisation
5. Génération de rapports
6. Questions/Réponses

Commandes:
- python -m src.main run --data PATH [--config config.yaml] [--outdir outputs]
- python -m src.main ask --data PATH --question "..."

Utilise le module pipeline.run_pipeline() pour éviter la duplication.
"""

import sys
import os
import logging
import argparse
import json
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import yaml

from src.pipeline import run_pipeline
from src.qa import DataQA
from src.config_env import load_dotenv_config, get_openai_key, is_llm_enabled as llm_enabled

# Configuration par défaut
DEFAULT_CONFIG_PATH = "config.yaml"
DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_LOG_LEVEL = "INFO"


def setup_logging(log_level: str, outdir: str = "outputs") -> logging.Logger:
    """
    Configure le système de logging.

    Args:
        log_level: Niveau de logging (DEBUG, INFO, WARNING, ERROR)
        outdir: Répertoire de sortie pour les logs

    Returns:
        logging.Logger: Logger configuré
    """
    log_path = Path(outdir) / "logs" / "analyst.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers = [logging.StreamHandler(sys.stdout)]
    handlers.append(logging.FileHandler(log_path))

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        handlers=handlers,
        force=True
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configuré avec niveau: {log_level}")
    logger.info(f"Répertoire de sortie: {outdir}")
    return logger


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Charge la configuration depuis un fichier YAML.

    Args:
        config_path: Chemin vers le fichier config.yaml

    Returns:
        Dict: Configuration chargée
    """
    config_path = Path(config_path)

    if not config_path.exists():
        return {
            "data": {"output_dir": DEFAULT_OUTPUT_DIR},
            "llm": {"enabled": False},
            "cleaning": {"handle_duplicates": True, "handle_outliers": True},
            "visualization": {"style": "default"}
        }

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config or {}


def check_llm_config(config: Dict[str, Any], logger: logging.Logger) -> Dict[str, Any]:
    """
    Vérifie la configuration LLM et ajuste si nécessaire.

    Args:
        config: Configuration chargée
        logger: Logger

    Returns:
        Dict: Configuration ajustée
    """
    llm_config = config.get("llm", {})
    if not llm_config.get("enabled", False):
        logger.info("LLM désactivé dans la configuration")
        return config

    try:
        load_dotenv_config()
        key = get_openai_key()
        logger.info("Clé API OpenAI trouvée")
        return config
    except ValueError as e:
        logger.warning(f"Clé API OpenAI non disponible: {e}")
        logger.warning("Passage en mode LLM désactivé")
        config["llm"]["enabled"] = False
        return config


def main() -> int:
    """
    Point d'entrée principal.

    Returns:
        int: Code de retour (0 = succès)
    """
    parser = argparse.ArgumentParser(
        description="Data Analyst Agent - Pipeline complète d'analyse de données",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python -m src.main run --data data/input.csv --config config.yaml --outdir outputs
  python -m src.main ask --data data/input.csv --question "Combien de lignes?"

Sous-commands:
  run     Exécute la pipeline complète d'analyse
  ask     Pose une question sur le dataset
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # Commande run
    run_parser = subparsers.add_parser("run", help="Exécute la pipeline complète")
    run_parser.add_argument("--data", required=True, help="Chemin vers le fichier CSV/Excel")
    run_parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Chemin vers config.yaml")
    run_parser.add_argument("--outdir", default=DEFAULT_OUTPUT_DIR, help="Répertoire de sortie")
    run_parser.add_argument("--log-level", default=DEFAULT_LOG_LEVEL,
                           choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                           help="Niveau de logging")

    # Commande ask
    ask_parser = subparsers.add_parser("ask", help="Pose une question")
    ask_parser.add_argument("--data", required=True, help="Chemin vers le fichier CSV/Excel")
    ask_parser.add_argument("--question", required=True, help="La question à poser")
    ask_parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Chemin vers config.yaml")
    ask_parser.add_argument("--outdir", default=DEFAULT_OUTPUT_DIR, help="Répertoire de sortie")
    ask_parser.add_argument("--log-level", default=DEFAULT_LOG_LEVEL,
                           choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                           help="Niveau de logging")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Charger la config
    config = load_config(args.config)

    # Setup logging
    logger = setup_logging(args.log_level, outdir=args.outdir)

    # Vérifier la config LLM
    config = check_llm_config(config, logger)

    logger.info(f"Data Analyst Agent - {args.command.upper()}")
    logger.info(f"Config chargée depuis: {args.config}")
    logger.info(f"LLM activé: {config.get('llm', {}).get('enabled', False)}")

    try:
        if args.command == "run":
            # Utiliser run_pipeline pour éviter la duplication
            results = run_pipeline(
                data_path=args.data,
                config_path=args.config,
                outdir=args.outdir
            )

            # Résumé des résultats
            figures = results.get("figures", {})
            figures_count = sum(len(v) for v in figures.values() if isinstance(v, list))

            print(f"\n{'=' * 50}")
            print("Analyse complétée avec succès!")
            print(f"{'=' * 50}")
            print(f"Résultats dans: {args.outdir}")
            print(f"- cleaned.csv: Données nettoyées")
            print(f"- summary.json: Résumé complet de l'analyse")
            print(f"- report.md: Rapport Markdown")
            print(f"- figures/: {figures_count} visualisations")

            return 0

        elif args.command == "ask":
            # Load data for QA
            from src.ingest import load_data
            df, ingestion_meta = load_data(args.data)
            logger.info(f"Dataset chargé: {df.shape[0]} lignes, {df.shape[1]} colonnes")

            # Load cleaned data if available
            cleaned_path = Path(args.outdir) / "cleaned.csv"
            if cleaned_path.exists():
                df_clean = pd.read_csv(cleaned_path)
                logger.info(f"Données nettoyées rechargées: {df_clean.shape[0]} lignes")
            else:
                df_clean = df

            # Initialiser le système QA
            qa_system = DataQA(df_clean, config)
            logger.info(f"Mode QA: {'LLM' if qa_system.llm_enabled else 'rule-based'}")

            # Poser la question
            response = qa_system.answer(args.question, return_tool_results=True)

            # Afficher la réponse
            if isinstance(response, dict):
                if "response" in response:
                    print(f"\n{response['response']}")
                if "error" in response:
                    print(f"\nErreur: {response['error']}")
                if "mode" in response:
                    print(f"[Mode: {response['mode']}]")
            else:
                print(f"\n{response}")

            # Sauvegarder la réponse
            answer_file = Path(args.outdir) / "last_answer.json"
            with open(answer_file, "w", encoding="utf-8") as f:
                json.dump({"question": args.question, "response": response}, f, indent=2, default=str)

            return 0

        else:
            parser.print_help()
            return 1

    except FileNotFoundError as e:
        logger.error(f"Fichier introuvable: {e}")
        print(f"\nErreur: {e}")
        print(f"Le fichier '{args.data}' est introuvable.")
        return 1

    except EmptyCSVError as e:
        logger.error(f"Fichier CSV vide: {e}")
        print(f"\nErreur: Le fichier '{args.data}' est vide.")
        return 1

    except ValueError as e:
        if "Clé API" in str(e):
            logger.error(f"Erreur configuration: {e}")
            print(f"\nErreur: Clé API OpenAI non configurée")
            print(f"\nVeuillez:")
            print(f"  1. Copier .env.example vers .env:")
            print(f"     copy .env.example .env  # Windows")
            print(f"     cp .env.example .env    # Linux/Mac")
            print(f"  2. Remplir votre clé API dans .env:")
            print(f"     OPENAI_API_KEY=sk-votre_cle_ici")
            return 1
        else:
            logger.error(f"Erreur: {e}")
            print(f"\nErreur: {e}")
            return 1

    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        print(f"\nErreur fatale: {e}")
        return 1


# Exceptions personnalisées
class EmptyCSVError(Exception):
    """Exception levée lorsqu'un fichier CSV est vide."""
    pass


if __name__ == "__main__":
    sys.exit(main())
