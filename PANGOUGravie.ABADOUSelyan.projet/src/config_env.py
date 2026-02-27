"""
Module de configuration via environment variables.

Ce module charge la configuration depuis un fichier .env
et fournit des fonctions pour accéder aux clés sensibles.
"""

import os
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Résoudre le chemin du fichier .env
# Cherche d'abord dans le répertoire courant, puis dans le répertoire parent
def _find_dotenv() -> Optional[Path]:
    """Trouve le fichier .env dans le répertoire courant ou parent."""
    current = Path.cwd()
    max_depth = 3  # Limiter la recherche à 3 niveaux

    for _ in range(max_depth):
        dotenv_path = current / ".env"
        if dotenv_path.exists():
            return dotenv_path
        # Remonter d'un niveau
        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def load_dotenv_config() -> bool:
    """
    Charge la configuration depuis .env si disponible.

    Returns:
        bool: True si .env a été chargé, False sinon
    """
    dotenv_path = _find_dotenv()

    if dotenv_path:
        load_dotenv(dotenv_path=dotenv_path)
        logger.info(f"Configuration chargée depuis: {dotenv_path}")
        return True
    else:
        logger.warning("Fichier .env non trouvé. La clé API OpenAI ne sera pas disponible.")
        return False


def get_openai_key() -> str:
    """
    Récupère la clé API OpenAI depuis les variables d'environnement.

    Returns:
        str: La clé API OpenAI

    Raises:
        ValueError: Si la clé API n'est pas configurée
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or api_key == "your_api_key_here":
        env_path = _find_dotenv()
        error_msg = (
            "Clé API OpenAI non configurée.\n\n"
            "Veuillez:\n"
            "1. Copier .env.example vers .env:\n"
            "   cp .env.example .env  # Linux/Mac\n"
            "   copy .env.example .env  # Windows\n"
            "2. Remplir votre clé API dans .env:\n"
            "   OPENAI_API_KEY=sk-votre_cle_ici\n"
        )

        if env_path:
            error_msg += f"\nFichier .env trouvé: {env_path}\n"
        else:
            error_msg += "\nFichier .env non trouvé. Créez-en un dans le répertoire racine.\n"

        logger.error("OPENAI_API_KEY non trouvée")
        raise ValueError(error_msg)

    logger.info("Clé API OpenAI chargée depuis environment")
    return api_key


def is_llm_enabled(config: Optional[dict] = None) -> bool:
    """
    Vérifie si le mode LLM est activé.

    Args:
        config: Configuration optionnelle (ex: depuis config.yaml)

    Returns:
        bool: True si LLM est activé
    """
    if config is None:
        return False

    return config.get("llm", {}).get("enabled", False)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("Test de configuration:")
    loaded = load_dotenv_config()
    print(f".env chargé: {loaded}")

    try:
        key = get_openai_key()
        print(f"Clé API: {key[:10]}...{key[-4:] if len(key) > 14 else ''}")
    except ValueError as e:
        print(f"Erreur: {e}")
