"""
Module de wrapper OpenAI Responses API.

Ce module fournit une abstraction pour utiliser l'API OpenAI avec
tool calling pour l'analyse de données, en mode sécurisé.
"""

import os
import json
import logging
import re
from typing import Optional, Dict, Any, List, Tuple, Union
from datetime import datetime
from pathlib import Path

from src.config_env import get_openai_key

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Exception levée lors d'une erreur avec l'API LLM."""
    pass


class LLMConfigError(LLMError):
    """Exception levée lors d'une erreur de configuration."""
    pass


def llm_enabled(config: Optional[Dict[str, Any]] = None) -> bool:
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


class OpenAIWrapper:
    """
    Wrapper pour l'API OpenAI Responses API.

    Gère:
    - Configuration sécurisée (clé depuis config_env.get_openai_key())
    - Tool calling pour l'analyse de données
    - Limites de sécurité
    - Gestion des erreurs
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialise le wrapper OpenAI.

        Args:
            config: Configuration optionnelle (ex: {'model': 'gpt-4o', 'enabled': True})
        """
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.model = self.config.get('model', 'gpt-4o')
        self.max_context_tokens = self.config.get('max_context_tokens', 128000)
        self.max_output_tokens = self.config.get('max_output_tokens', 4096)
        self.temperature = self.config.get('temperature', 0.3)

        # Sécurité
        self.security = self.config.get('security', {})
        self.prevent_code_execution = self.security.get('prevent_code_execution', True)
        self.max_query_cost = self.security.get('max_query_cost', 0.10)
        self.max_queries_per_minute = self.security.get('max_queries_per_minute', 10)

        # Récupérer la clé via config_env
        self.api_key = None
        self.client = None

        # Stats
        self.query_count = 0
        self.total_cost_estimate = 0.0

        if self.enabled:
            try:
                self.api_key = get_openai_key()
                self._init_client()
            except ValueError as e:
                logger.warning(f"Configuration LLM incomplète: {e}")
                self.enabled = False
            except Exception as e:
                logger.warning(f"Erreur initialisation LLM: {e}")
                self.enabled = False

    def _init_client(self) -> None:
        """Initialise le client OpenAI."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("Client OpenAI initialisé")
        except ImportError:
            logger.error("Package openai non installé. Install: pip install openai")
            raise LLMConfigError("Package openai requis. Install: pip install openai")
        except Exception as e:
            logger.error(f"Erreur initialisation OpenAI: {e}")
            raise LLMError(f"Erreur OpenAI: {e}")

    def _estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Estime le coût d'une requête (approximatif).

        Utilise les prix GPT-4o comme référence.
        """
        input_price = 2.50   # $2.50 per 1M input tokens
        output_price = 10.00  # $10.00 per 1M output tokens

        cost = (prompt_tokens / 1_000_000) * input_price + \
               (completion_tokens / 1_000_000) * output_price
        return cost

    def _validate_tool(self, tool_name: str, args: Dict[str, Any]) -> bool:
        """
        Valide un outil avant exécution.

        Empêche l'exécution de code arbitraire.
        """
        allowed_tools = {
            'analyze_data', 'get_column_stats', 'find_correlations',
            'generate_plot', 'generate_report', 'compute_statistics',
            'filter_data', 'describe_dataset', 'get_data_summary'
        }

        if tool_name not in allowed_tools:
            logger.error(f"Outil non autorisé: {tool_name}")
            return False

        if self.prevent_code_execution:
            for value in args.values():
                if isinstance(value, str):
                    dangerous_patterns = ['__import__', 'exec(', 'eval(', 'os.system', 'subprocess', 'popen']
                    if any(p in value for p in dangerous_patterns):
                        logger.error(f"Code potentiellement dangereux détecté dans {tool_name}")
                        return False

        return True

    def run_text_query(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto"
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Exécute une requête textuelle avec l'API OpenAI.

        Args:
            system_prompt: Le prompt système
            user_prompt: Le prompt utilisateur
            tools: Liste des outils disponibles
            tool_choice: "auto", "none", ou nom d'un outil

        Returns:
            Tuple: (tool_calls_data, text_response)
        """
        if not self.enabled or not self.client:
            return None, None

        if self.query_count >= self.max_queries_per_minute:
            logger.error("Limite de requêtes par minute atteinte")
            raise LLMError("Trop de requêtes. Attendez une minute.")

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools or [],
                tool_choice=tool_choice,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature,
                n=1
            )

            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            cost = self._estimate_cost(prompt_tokens, completion_tokens)
            self.total_cost_estimate += cost

            if cost > self.max_query_cost:
                logger.error(f"Coût trop élevé: ${cost:.4f}")
                raise LLMError(f"Coût trop élevé: ${cost:.4f}")

            self.query_count += 1

            message = response.choices[0].message

            if message.tool_calls:
                tool_calls = []
                for tc in message.tool_calls:
                    tool_calls.append({
                        'id': tc.id,
                        'name': tc.function.name,
                        'arguments': tc.function.arguments
                    })
                return {'tool_calls': tool_calls}, None
            elif message.content:
                return None, message.content
            else:
                return None, None

        except Exception as e:
            logger.error(f"Erreur lors de l'appel LLM: {e}")
            raise LLMError(f"Erreur LLM: {e}")

    def run_json_query(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Exécute une requête qui doit retourner du JSON.

        Args:
            system_prompt: Le prompt système
            user_prompt: Le prompt utilisateur
            response_format: Format attendu pour la réponse JSON

        Returns:
            dict: Le JSON parsé de la réponse
        """
        if not self.enabled or not self.client:
            raise LLMError("LLM non initialisé")

        try:
            # Ajouter "json" dans le prompt pour respecter l'exigence OpenAI
            # quand response_format est json_object
            user_prompt_with_json = (
                f"{user_prompt}\n\n"
                "IMPORTANT: Réponds UNIQUEMENT avec du JSON. "
                "N'inclue aucun texte autre que le JSON demandé."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt_with_json}
            ]

            # Forcer le format JSON
            json_format = {
                "type": "json_object"
            }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format=json_format,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature,
                n=1
            )

            content = response.choices[0].message.content

            # Parsing robuste du JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback: extraire le JSON entre { et }
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                raise LLMError("Impossible de parser la réponse JSON")

        except Exception as e:
            logger.error(f"Erreur lors de la requête JSON: {e}")
            raise LLMError(f"Erreur LLM JSON: {e}")

    def ask_analysis_question(
        self,
        question: str,
        context: Dict[str, Any],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Pose une question d'analyse avec contexte.

        Args:
            question: La question posée
            context: Contexte du dataset
            tools: Liste des outils disponibles

        Returns:
            Tuple: (tool_calls, response_text)
        """
        default_tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_data",
                    "description": "Analyse les données et retourne des statistiques",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "columns": {"type": "array", "items": {"type": "string"}},
                            "metric": {"type": "string", "enum": ["mean", "median", "min", "max", "count", "std"]}
                        },
                        "required": ["columns", "metric"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_data_summary",
                    "description": "Fournit un résumé complet du dataset",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "filter_data",
                    "description": "Filtre les données selon une condition",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "column": {"type": "string"},
                            "operator": {"type": "string", "enum": [">", "<", "==", ">=", "<=", "!="]},
                            "value": {"type": ["string", "number"]}
                        },
                        "required": ["column", "operator", "value"]
                    }
                }
            }
        ]

        tools_to_use = tools if tools else default_tools

        context_text = f"""
Dataset:
- Lignes: {context.get('rows', 'N/A')}
- Colonnes: {context.get('columns', [])}
- Types: {context.get('dtypes', {})}
"""

        system_prompt = f"""Tu es un assistant d'analyse de données expert.

Dataset disponible:
{context_text}

Instructions:
1. Analyse la question de l'utilisateur
2. Choisis l'outil approprié
3. Fournis une réponse claire et concise
4. Ne jamais exécuter de code arbitraire
"""

        return self.run_text_query(system_prompt, question, tools_to_use)


def run_llm_text(config: Dict[str, Any], system_prompt: str, user_prompt: str) -> str:
    """
    Exécute une requête texte avec l'API OpenAI.

    Args:
        config: Configuration LLM (ex: config['llm'])
        system_prompt: Le prompt système
        user_prompt: Le prompt utilisateur

    Returns:
        str: La réponse textuelle de l'LLM
    """
    if not llm_enabled(config):
        raise LLMError("LLM désactivé dans la configuration")

    # Extraire la sous-configuration llm si elle existe
    llm_config = config.get('llm', config) if isinstance(config, dict) and 'llm' in config else config
    wrapper = OpenAIWrapper(llm_config)
    if not wrapper.enabled:
        raise LLMError("LLM non disponible (pas de clé API)")

    _, response = wrapper.run_text_query(system_prompt, user_prompt)
    return response or "Pas de réponse de l'LLM"


def run_llm_json(config: Dict[str, Any], system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    """
    Exécute une requête JSON avec l'API OpenAI.

    Args:
        config: Configuration LLM (ex: {'llm': {'enabled': True, 'model': 'gpt-4o'}})
        system_prompt: Le prompt système
        user_prompt: Le prompt utilisateur

    Returns:
        dict: Le JSON parsé de la réponse
    """
    if not llm_enabled(config):
        raise LLMError("LLM désactivé dans la configuration")

    # Extraire la sous-configuration llm si elle existe
    llm_config = config.get('llm', config) if isinstance(config, dict) and 'llm' in config else config
    wrapper = OpenAIWrapper(llm_config)
    if not wrapper.enabled:
        raise LLMError("LLM non disponible (pas de clé API)")

    return wrapper.run_json_query(system_prompt, user_prompt)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    print("Test du wrapper OpenAI")

    # Charger la config
    import yaml
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    llm_config = config.get("llm", {})

    print(f"LLM enabled: {llm_enabled(llm_config)}")

    try:
        wrapper = OpenAIWrapper(llm_config)
        print(f"API key configured: {wrapper.api_key is not None}")

        if wrapper.enabled:
            print("Client OpenAI initialisé")
            print(f"Modèle: {wrapper.model}")
        else:
            print("Fallback en mode rule-based")
    except Exception as e:
        print(f"Erreur: {e}")
