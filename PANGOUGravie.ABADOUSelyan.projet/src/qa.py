"""
Module de Questions/Réponses naturelles (QA).

Ce module fournit un système d'agent LLM pour répondre à des questions en
langage naturel sur un jeu de données.

Principe:
- Le LLM ne fait que décider quels outils appeler
- Le code exécute les outils (pandas) et renvoie les résultats
- Interdiction d'exec arbitraire

Outils autorisés:
- get_schema()
- get_missingness()
- describe_column(col)
- top_categories(col, n)
- correlation(col_x, col_y)
- groupby_agg(group_col, target_col, agg)
- time_aggregate(date_col, freq)

Fallback:
- si LLM off: intent parsing basique avec difflib pour fuzzy match colonnes
"""

import pandas as pd
import numpy as np
import logging
import difflib
import json
from pathlib import Path
from typing import Optional, Union, Dict, Any, List, Tuple
from datetime import datetime

from src.config_env import is_llm_enabled as llm_enabled
from src.llm import run_llm_json, LLMError

logger = logging.getLogger(__name__)


class DataQA:
    """
    Classe principale pour le système de Questions/Réponses sur les données.

    Fournit des réponses à des questions en langage naturel sur un DataFrame.
    Supporte le mode LLM (avec tool calling) et le mode rule-based en fallback.
    """

    # Outils autorisés avec leurs signatures
    ALLOWED_TOOLS = {
        "get_schema": {
            "description": "Retourne la liste des colonnes avec leurs types",
            "returns": "Liste de {column, type} pour chaque colonne"
        },
        "get_missingness": {
            "description": "Retourne le nombre et pourcentage de valeurs manquantes par colonne",
            "returns": "Dictionnaire {colonne: {count, percentage}}"
        },
        "describe_column": {
            "description": "Retourne les statistiques descriptives d'une colonne (mean, median, min, max, std pour numériques; value counts pour catégorielles)",
            "parameters": {
                "column": {"type": "string", "description": "Nom de la colonne"}
            },
            "returns": "Dictionnaire avec les statistiques"
        },
        "top_categories": {
            "description": "Retourne les valeurs les plus fréquentes d'une colonne catégorielle",
            "parameters": {
                "column": {"type": "string", "description": "Nom de la colonne"},
                "n": {"type": "integer", "description": "Nombre de valeurs à retourner (défaut: 5)"}
            },
            "returns": "Liste de {value, count, percentage}"
        },
        "correlation": {
            "description": "Calcule le coefficient de corrélation de Pearson entre deux colonnes numériques",
            "parameters": {
                "column_x": {"type": "string", "description": "Première colonne"},
                "column_y": {"type": "string", "description": "Deuxième colonne"}
            },
            "returns": "Float: coefficient de corrélation (-1 à 1)"
        },
        "groupby_agg": {
            "description": "Effectue un groupby avec une aggregation (mean, sum, count, median, min, max)",
            "parameters": {
                "group_column": {"type": "string", "description": "Colonne de groupement"},
                "target_column": {"type": "string", "description": "Colonne à agréger"},
                "aggregation": {"type": "string", "enum": ["mean", "sum", "count", "median", "min", "max"], "description": "Type d'aggregation"}
            },
            "returns": "DataFrame avec les résultats groupés"
        },
        "time_aggregate": {
            "description": "Aggrège les données temporelles par jour/semaine/mois",
            "parameters": {
                "date_column": {"type": "string", "description": "Colonne de date"},
                "frequency": {"type": "string", "enum": ["D", "W", "M"], "description": "Fréquence: D=jour, W=semaine, M=mois"}
            },
            "returns": "Série temporelle agrégée"
        }
    }

    # Aggregations autorisées
    ALLOWED_AGGREGATIONS = ["mean", "sum", "count", "median", "min", "max"]

    def __init__(self, df: pd.DataFrame, config: Optional[Dict[str, Any]] = None):
        """
        Initialise le système QA.

        Args:
            df: Le DataFrame à interroger
            config: Configuration optionnelle (ex: {'llm': {'enabled': True}})
        """
        self.df = df.copy()
        self.config = config or {}
        self.history: List[Dict[str, Any]] = []
        self._summary_cache: Optional[Dict[str, Any]] = None

        # Type de chaque colonne
        self.column_types = self._infer_column_types()

        # Configuration LLM
        self.llm_config = self.config.get('llm', {'enabled': False})
        self.llm_enabled = llm_enabled(self.llm_config)

        # Contexte pour les requêtes LLM
        self.context = self._build_context()

        logger.info(f"DataQA initialisé ({'LLM' if self.llm_enabled else 'rule-based'}): {len(df.columns)} colonnes")

    def _infer_column_types(self) -> Dict[str, str]:
        """Infère le type de chaque colonne."""
        column_types = {}
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                column_types[col] = "numeric"
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                column_types[col] = "datetime"
            else:
                column_types[col] = "categorical"
        return column_types

    def _build_context(self) -> Dict[str, Any]:
        """Construit le contexte compact pour les requêtes LLM."""
        column_infos = []
        for col in self.df.columns:
            col_type = self.column_types.get(col, "unknown")
            column_infos.append({
                "name": col,
                "type": col_type,
                "sample_values": self._get_sample_values(col, 3)
            })

        return {
            'rows': len(self.df),
            'columns': column_infos,
            'memory_bytes': int(self.df.memory_usage(deep=True).sum())
        }

    def _get_sample_values(self, col: str, n: int = 3) -> List[str]:
        """Obtient des valeurs d'échantillon pour une colonne."""
        series = self.df[col].dropna()
        if len(series) == 0:
            return []
        # Limiter la longueur des strings
        samples = series.head(n).astype(str).tolist()
        return [str(s)[:50] for s in samples]

    # === Outils exécutés par le code (pas par LLM) ===

    def _tool_get_schema(self) -> List[Dict[str, str]]:
        """Outil: retourne le schéma du DataFrame."""
        return [
            {"column": col, "type": self.column_types.get(col, "unknown")}
            for col in self.df.columns
        ]

    def _tool_get_missingness(self) -> Dict[str, Dict[str, float]]:
        """Outil: retourne la missingness par colonne."""
        result = {}
        for col in self.df.columns:
            count = int(self.df[col].isnull().sum())
            percentage = float((self.df[col].isnull().mean() * 100) if len(self.df) > 0 else 0)
            result[col] = {"count": count, "percentage": percentage}
        return result

    def _tool_describe_column(self, column: str) -> Dict[str, Any]:
        """Outil: retourne les statistiques d'une colonne."""
        if column not in self.df.columns:
            return {"error": f"Colonne '{column}' introuvable"}

        series = self.df[column].dropna()
        col_type = self.column_types.get(column, "unknown")

        if col_type == "numeric":
            return {
                "column": column,
                "type": col_type,
                "count": int(len(series)),
                "mean": float(series.mean()) if len(series) > 0 else None,
                "median": float(series.median()) if len(series) > 0 else None,
                "std": float(series.std()) if len(series) > 0 else None,
                "min": float(series.min()) if len(series) > 0 else None,
                "max": float(series.max()) if len(series) > 0 else None,
                "skewness": float(series.skew()) if len(series) > 1 else None,
                "kurtosis": float(series.kurt()) if len(series) > 1 else None
            }
        elif col_type == "categorical":
            value_counts = series.value_counts(dropna=False)
            top_values = []
            for val, count in value_counts.head(5).items():
                pct = (count / len(series)) * 100 if len(series) > 0 else 0
                top_values.append({
                    "value": str(val) if val is not None else "null",
                    "count": int(count),
                    "percentage": float(pct)
                })
            return {
                "column": column,
                "type": col_type,
                "count": int(len(series)),
                "unique": int(series.nunique()),
                "top_values": top_values
            }
        elif col_type == "datetime":
            return {
                "column": column,
                "type": col_type,
                "count": int(len(series)),
                "min": str(series.min()),
                "max": str(series.max()),
                "range_days": int((series.max() - series.min()).days) if len(series) > 0 else 0
            }
        else:
            return {"column": column, "type": col_type, "count": int(len(series)), "error": "Type non reconnu"}

    def _tool_top_categories(self, column: str, n: int = 5) -> List[Dict[str, Any]]:
        """Outil: retourne les catégories les plus fréquentes."""
        if column not in self.df.columns:
            return [{"error": f"Colonne '{column}' introuvable"}]

        if self.column_types.get(column) != "categorical":
            return [{"error": f"Colonne '{column}' n'est pas catégorielle"}]

        value_counts = self.df[column].value_counts(dropna=False)
        result = []
        for val, count in value_counts.head(n).items():
            pct = (count / len(self.df)) * 100 if len(self.df) > 0 else 0
            result.append({
                "value": str(val) if val is not None else "null",
                "count": int(count),
                "percentage": float(pct)
            })
        return result

    def _tool_correlation(self, column_x: str, column_y: str) -> Dict[str, Any]:
        """Outil: calcule la corrélation entre deux colonnes."""
        if column_x not in self.df.columns:
            return {"error": f"Colonne '{column_x}' introuvable"}
        if column_y not in self.df.columns:
            return {"error": f"Colonne '{column_y}' introuvable"}

        if self.column_types.get(column_x) != "numeric" or self.column_types.get(column_y) != "numeric":
            return {"error": "Les deux colonnes doivent être numériques pour calculer la corrélation"}

        # Dropped NA pour le calcul
        data = self.df[[column_x, column_y]].dropna()
        if len(data) < 2:
            return {"error": "Pas assez de données non-na pour calculer la corrélation"}

        corr = data[column_x].corr(data[column_y])
        return {
            "column_x": column_x,
            "column_y": column_y,
            "correlation": float(corr) if not pd.isna(corr) else None,
            "sample_size": int(len(data))
        }

    def _tool_groupby_agg(
        self,
        group_column: str,
        target_column: str,
        aggregation: str
    ) -> Dict[str, Any]:
        """Outil: effectue un groupby avec aggregation."""
        if group_column not in self.df.columns:
            return {"error": f"Colonne de groupement '{group_column}' introuvable"}
        if target_column not in self.df.columns:
            return {"error": f"Colonne cible '{target_column}' introuvable"}
        if aggregation not in self.ALLOWED_AGGREGATIONS:
            return {"error": f"Aggregation '{aggregation}' non autorisée. Choix: {self.ALLOWED_AGGREGATIONS}"}

        group_series = self.df[group_column]
        target_series = self.df[target_column]

        # Supprimer les NA pour le groupby
        valid_mask = group_series.notna() & target_series.notna()
        valid_df = self.df[valid_mask]

        if len(valid_df) == 0:
            return {"error": "Aucune donnée valide pour le groupby"}

        try:
            if aggregation == "count":
                result = valid_df.groupby(group_column)[target_column].count()
            elif aggregation == "sum":
                result = valid_df.groupby(group_column)[target_column].sum()
            elif aggregation == "mean":
                result = valid_df.groupby(group_column)[target_column].mean()
            elif aggregation == "median":
                result = valid_df.groupby(group_column)[target_column].median()
            elif aggregation == "min":
                result = valid_df.groupby(group_column)[target_column].min()
            elif aggregation == "max":
                result = valid_df.groupby(group_column)[target_column].max()

            # Convertir en liste de dictionnaires
            result_list = []
            for group_val, agg_val in result.items():
                result_list.append({
                    "group": str(group_val),
                    aggregation: float(agg_val) if pd.api.types.is_numeric_dtype(type(agg_val)) else agg_val
                })
            return {"results": result_list, "aggregation": aggregation, "group_column": group_column, "target_column": target_column}
        except Exception as e:
            return {"error": f"Erreur lors du groupby: {str(e)}"}

    def _tool_time_aggregate(self, date_column: str, frequency: str) -> Dict[str, Any]:
        """Outil: agrège les données temporelles."""
        if date_column not in self.df.columns:
            return {"error": f"Colonne de date '{date_column}' introuvable"}

        if self.column_types.get(date_column) != "datetime":
            # Tenter la conversion
            try:
                self.df[date_column] = pd.to_datetime(self.df[date_column], errors='raise')
                self.column_types[date_column] = "datetime"
            except Exception:
                return {"error": f"Colonne '{date_column}' n'est pas une date valide"}

        # Dropped NA
        valid_df = self.df[[date_column]].dropna()

        if len(valid_df) == 0:
            return {"error": "Aucune donnée de date valide"}

        # Déterminer la fréquence
        freq_map = {"D": "D", "W": "W-MON", "M": "M"}
        pd_freq = freq_map.get(frequency, "M")

        try:
            # Créer une colonne d'année-mois ou d'année-mois-jour
            if frequency == "D":
                valid_df['period'] = valid_df[date_column].dt.strftime('%Y-%m-%d')
            elif frequency == "W":
                valid_df['period'] = valid_df[date_column].dt.to_period('W').astype(str)
            else:  # M
                valid_df['period'] = valid_df[date_column].dt.to_period('M').astype(str)

            # Compter les occurrences par période
            counts = valid_df['period'].value_counts().sort_index()

            result_list = []
            for period, count in counts.items():
                result_list.append({
                    "period": period,
                    "count": int(count)
                })

            return {"results": result_list, "frequency": frequency, "date_column": date_column}
        except Exception as e:
            return {"error": f"Erreur lors de l'agrégation temporelle: {str(e)}"}

    # === Agent LLM ===

    def _fuzzy_match_column(self, column_name: str, threshold: float = 0.6) -> Optional[str]:
        """
        Fuzzy match d'une colonne avec les colonnes du DataFrame.
        Utilise difflib pour trouver la colonne la plus proche.

        Args:
            column_name: Le nom de colonne à matcher
            threshold: Seuil de similarité (0 à 1)

        Returns:
            Le nom de colonne matched ou None
        """
        available_cols = list(self.column_types.keys())
        matches = difflib.get_close_matches(column_name.lower(), [c.lower() for c in available_cols], n=1, cutoff=threshold)

        if matches:
            # Trouver le nom original
            for col in available_cols:
                if col.lower() == matches[0]:
                    return col
        return None

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[Any, bool]:
        """
        Exécute un outil autorisé.

        Args:
            tool_name: Nom de l'outil
            arguments: Arguments de l'outil

        Returns:
            Tuple: (result, success)
        """
        # Vérifier que l'outil est autorisé
        if tool_name not in self.ALLOWED_TOOLS:
            return {"error": f"Outil '{tool_name}' non autorisé"}, False

        # Vérifier les arguments requis
        required_params = self.ALLOWED_TOOLS[tool_name].get("parameters", {})
        for param, spec in required_params.items():
            if spec.get("required", True) and param not in arguments:
                return {"error": f"Paramètre manquant: {param}"}, False

        # Mapping des outils vers les méthodes
        tool_methods = {
            "get_schema": lambda: self._tool_get_schema(),
            "get_missingness": lambda: self._tool_get_missingness(),
            "describe_column": lambda: self._tool_describe_column(arguments.get("column")),
            "top_categories": lambda: self._tool_top_categories(
                arguments.get("column", ""),
                arguments.get("n", 5)
            ),
            "correlation": lambda: self._tool_correlation(
                arguments.get("column_x", ""),
                arguments.get("column_y", "")
            ),
            "groupby_agg": lambda: self._tool_groupby_agg(
                arguments.get("group_column", ""),
                arguments.get("target_column", ""),
                arguments.get("aggregation", "")
            ),
            "time_aggregate": lambda: self._tool_time_aggregate(
                arguments.get("date_column", ""),
                arguments.get("frequency", "M")
            )
        }

        try:
            result = tool_methods[tool_name]()
            return result, True
        except Exception as e:
            logger.error(f"Erreur exécution tool {tool_name}: {e}")
            return {"error": f"Erreur: {str(e)}"}, False

    def _call_llm_for_tools(self, question: str) -> List[Dict[str, Any]]:
        """
        Appelle l'LLM pour décider quels outils appeler.

        Args:
            question: La question posée

        Returns:
            Liste des tool calls à exécuter
        """
        # Construire le prompt pour l'LLM
        context_text = f"""
Dataset: {len(self.df)} lignes, {len(self.df.columns)} colonnes

Types de colonnes:
- Numériques: {[col for col, t in self.column_types.items() if t == 'numeric'][:10]}
- Catégorielles: {[col for col, t in self.column_types.items() if t == 'categorical'][:10]}
- Dates: {[col for col, t in self.column_types.items() if t == 'datetime'][:5]}

Questions à traiter: {question}
"""

        system_prompt = """Tu es un assistant d'analyse de données expert.

Outils disponibles:
1. get_schema() - Liste des colonnes avec types
2. get_missingness() - Valeurs manquantes par colonne
3. describe_column(column) - Stats d'une colonne
4. top_categories(column, n) - Top n valeurs catégorielles
5. correlation(column_x, column_y) - Corrélation entre 2 colonnes numériques
6. groupby_agg(group_column, target_column, aggregation) - Groupby avec aggregation (mean/sum/count/median/min/max)
7. time_aggregate(date_column, frequency) - Agrégation temporelle (D/W/M)

Format de réponse:
{{
  "tools": [
    {{"tool": "nom_tool", "arguments": {{"param": "valeur", ...}}}}
  ]
}}

Règles:
- Choisisse au maximum 3 outils pertinents
- Pour les colonnes inconnues, propose un fuzzy match basé sur le contexte
- Ne jamais demander plus d'information à l'utilisateur
- Si pas d'outil pertinent, retourner tools: []
"""

        try:
            response = run_llm_json(
                self.llm_config,
                system_prompt,
                context_text
            )
            tools = response.get("tools", [])
            logger.info(f"LLM a sélectionné {len(tools)} outils")
            return tools
        except LLMError:
            logger.warning("LLM non disponible, fallback en mode rule-based")
            return []
        except Exception as e:
            logger.warning(f"Erreur LLM: {e}, fallback")
            return []

    def _generate_response_from_tools(
        self,
        question: str,
        tool_results: List[Tuple[str, Any, bool]]
    ) -> str:
        """
        Génère une réponse naturelle à partir des résultats des outils.

        Args:
            question: Question posée
            tool_results: [(tool_name, result, success)]

        Returns:
            str: La réponse générée
        """
        # Appeler l'LLM pour générer la réponse
        tools_text = []
        for tool_name, result, success in tool_results:
            status = "SUCCESS" if success else f"ERROR: {result.get('error', 'unknown')}"
            tools_text.append(f"[{tool_name}] {status}: {result}")

        context = f"""
Question: {question}

Résultats des outils:
{chr(10).join(tools_text)}
"""

        system_prompt = """Tu es un assistant d'analyse de données expert.

Rend une réponse claire, concise et en français à la question posée,
basée uniquement sur les résultats des outils fournis.

Format de réponse:
- Commencer par la réponse directe
- Puis ajouter "Comment calculé:" avec une brève explication
- Ne jamais mentir sur les données
- Si les données sont insuffisantes, le dire clairement

Exemple:
"Le prix moyen est de 150€. Comment calculé: moyenne des valeurs de la colonne 'prix' après suppression des valeurs manquantes."
"""

        try:
            response = run_llm_json(
                self.llm_config,
                system_prompt,
                context
            )
            # Si LLM retourne du JSON avec "response"
            if isinstance(response, dict) and "response" in response:
                return response["response"]
            elif isinstance(response, str):
                return response
            return str(response)
        except Exception as e:
            logger.warning(f"Erreur génération réponse LLM: {e}, fallback")

            # Fallback: construire la réponse manuellement
            return self._generate_fallback_response(question, tool_results)

    def _generate_fallback_response(
        self,
        question: str,
        tool_results: List[Tuple[str, Any, bool]]
    ) -> str:
        """Génère une réponse en mode rule-based si LLM échoue."""
        if not tool_results:
            return "Je n'ai pas pu analyser votre question avec les outils disponibles."

        # Extraire les résultats utiles
        responses = []
        for tool_name, result, success in tool_results:
            if success:
                if tool_name == "get_schema":
                    cols = [f"{r['column']} ({r['type']})" for r in result]
                    responses.append(f"Colonnes disponibles: {', '.join(cols)}")
                elif tool_name == "get_missingness":
                    total_na = sum(v['count'] for v in result.values())
                    total_cells = len(self.df) * len(self.df.columns)
                    pct = (total_na / total_cells * 100) if total_cells > 0 else 0
                    responses.append(f"{total_na} valeurs manquantes ({pct:.1f}% du total)")
                elif tool_name == "describe_column":
                    col = result.get('column', 'inconnue')
                    if result.get('type') == 'numeric':
                        mean = result.get('mean', 'N/A')
                        responses.append(f"Colonne '{col}': moyenne = {mean}")
                    else:
                        top = result.get('top_values', [])
                        if top:
                            responses.append(f"Colonne '{col}': top = {top[0].get('value', 'N/A')}")
                elif tool_name == "top_categories":
                    col = result[0].get('error', '').replace("Colonne '", '').replace("' introuvable", '')
                    if col in self.df.columns:
                        col = col
                    else:
                        col = "colonne"
                    responses.append(f"Valeurs fréquentes de '{col}'")
                elif tool_name == "correlation":
                    col_x = result.get('column_x', 'X')
                    col_y = result.get('column_y', 'Y')
                    corr = result.get('correlation', 'N/A')
                    responses.append(f"Corrélation {col_x} vs {col_y}: {corr}")
                elif tool_name == "groupby_agg":
                    agg = result.get('aggregation', 'unknown')
                    col = result.get('group_column', 'col')
                    results = result.get('results', [])
                    if results:
                        first = results[0]
                        group_val = first.get('group', 'N/A')
                        agg_val = first.get(agg, 'N/A')
                        responses.append(f"Groupby '{col}' par {agg}: {group_val} -> {agg_val}")
                elif tool_name == "time_aggregate":
                    freq = result.get('frequency', '')
                    col = result.get('date_column', 'date')
                    responses.append(f"Série temporelle agrégée par {freq} pour '{col}'")

        if responses:
            answer = "; ".join(responses[:3])  # Limiter à 3 informations
            return f"Analyse: {answer}. Comment calculé: via les outils d'analyse pandas."
        else:
            return "Je n'ai pas pu extraire d'information significative de l'analyse."

    # === Mode rule-based (fallback) ===

    def _parse_intent_rule_based(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Parse l'intent en mode rule-based (fallback).

        Args:
            question: La question posée

        Returns:
            Dict avec tool_name et arguments ou None
        """
        question_lower = question.lower()

        # Count rows
        if any(kw in question_lower for kw in ["combien de lignes", "taille", "nombre de lignes", "lignes total"]):
            return {"tool": "get_schema", "arguments": {}}

        # Missingness
        if any(kw in question_lower for kw in ["valeurs manquantes", "missing", "nan", "données manquantes"]):
            return {"tool": "get_missingness", "arguments": {}}

        # Summary
        if any(kw in question_lower for kw in ["résumé", "description", "général", "snapshot"]):
            return {"tool": "get_schema", "arguments": {}}

        # Top categories
        if any(kw in question_lower for kw in ["plus fréquent", "top", "principale", "majorité"]):
            # Trouver une colonne catégorielle
            cat_cols = [c for c, t in self.column_types.items() if t == "categorical"]
            if cat_cols:
                col = self._fuzzy_match_column(question, 0.4) or cat_cols[0]
                return {"tool": "top_categories", "arguments": {"column": col, "n": 5}}

        # Statistics
        if any(kw in question_lower for kw in ["moyenne", "moyen", "moyen", "moyennes"]):
            num_cols = [c for c, t in self.column_types.items() if t == "numeric"]
            if num_cols:
                col = self._fuzzy_match_column(question, 0.4) or num_cols[0]
                return {"tool": "describe_column", "arguments": {"column": col}}

        # Correlation
        if any(kw in question_lower for kw in ["corrélé", "corrélation", "lié à", "correlation"]):
            num_cols = [c for c, t in self.column_types.items() if t == "numeric"]
            if len(num_cols) >= 2:
                return {"tool": "correlation", "arguments": {"column_x": num_cols[0], "column_y": num_cols[1]}}

        # Groupby
        if any(kw in question_lower for kw in ["par", "groupe", "grouper", "moyenne par", "somme par"]):
            group_cols = [c for c, t in self.column_types.items() if t in ["categorical", "datetime"]]
            target_cols = [c for c, t in self.column_types.items() if t == "numeric"]
            if group_cols and target_cols:
                group_col = self._fuzzy_match_column(question, 0.4) or group_cols[0]
                target_col = self._fuzzy_match_column(question, 0.4) or target_cols[0]
                return {"tool": "groupby_agg", "arguments": {"group_column": group_col, "target_column": target_col, "aggregation": "mean"}}

        # Time aggregate
        if any(kw in question_lower for kw in ["par jour", "par semaine", "par mois", "temporel", "évolution"]):
            date_cols = [c for c, t in self.column_types.items() if t == "datetime"]
            if date_cols:
                date_col = self._fuzzy_match_column(question, 0.4) or date_cols[0]
                if "jour" in question_lower:
                    return {"tool": "time_aggregate", "arguments": {"date_column": date_col, "frequency": "D"}}
                elif "semaine" in question_lower:
                    return {"tool": "time_aggregate", "arguments": {"date_column": date_col, "frequency": "W"}}
                else:
                    return {"tool": "time_aggregate", "arguments": {"date_column": date_col, "frequency": "M"}}

        return None

    def _answer_rule_based(self, question: str) -> str:
        """Répond en mode rule-based."""
        parsed = self._parse_intent_rule_based(question)

        if not parsed:
            return (
                "Je n'ai pas pu comprendre votre question. "
                "Vous pouvez demander:\n"
                "- 'Combien de lignes?'\n"
                "- 'Quelles sont les valeurs manquantes?'\n"
                "- 'Statistiques de [colonne]'\n"
                "- 'Valeurs plus fréquentes de [colonne]'\n"
                "- 'Corrélation entre [col1] et [col2]'\n"
                "- 'Moyenne par [catégorie]'\n"
                "- 'Évolution par jour/semaine/mois'"
            )

        tool_name = parsed["tool"]
        arguments = parsed["arguments"]
        result, success = self._execute_tool(tool_name, arguments)

        if not success:
            return f"Erreur lors de l'exécution: {result.get('error', 'unknown')}"

        # Générer une réponse simple
        if tool_name == "get_schema":
            cols = [f"{r['column']} ({r['type']})" for r in result]
            return f"Le DataFrame contient {len(self.df)} lignes et {len(cols)} colonnes: {', '.join(cols)}"
        elif tool_name == "get_missingness":
            total_na = sum(v['count'] for v in result.values())
            return f"Total: {total_na} valeurs manquantes sur {len(self.df) * len(self.df.columns)} cellules"
        elif tool_name == "describe_column":
            col = result.get('column', 'inconnue')
            if result.get('type') == 'numeric':
                mean = result.get('mean', 'N/A')
                return f"Colonne '{col}': moyenne = {mean}, médiane = {result.get('median', 'N/A')}. Comment calculé: statistiques pandas sur les valeurs non-null."
            else:
                top = result.get('top_values', [])
                if top:
                    val = top[0].get('value', 'N/A')
                    return f"Colonne '{col}': valeur principale = '{val}' ({top[0].get('count', 0)} occurrences)"
        elif tool_name == "top_categories":
            col = result[0].get('value', '') if result else ''
            if 'error' not in str(result[0]):
                return f"Valeurs principales: {col}"
        elif tool_name == "correlation":
            corr = result.get('correlation', 'N/A')
            return f"Corrélation = {corr}. Comment calculé: coefficient de Pearson entre les deux colonnes."
        elif tool_name == "groupby_agg":
            agg = result.get('aggregation', 'N/A')
            return f"Groupby effectué par {agg}."
        elif tool_name == "time_aggregate":
            freq = result.get('frequency', 'N/A')
            return f"Série temporelle agrégée par {freq}."

        return "Analyse complétée."

    # === Méthode principale ===

    def answer(self, question: str, return_tool_results: bool = False) -> Union[str, Dict[str, Any]]:
        """
        Répond à une question en langage naturel.

        Principe:
        - LLM decide quels outils appeler
        - Code exécute les outils et renvoie les résultats
        - LLM (ou fallback) génère la réponse finale

        Args:
            question: La question posée
            return_tool_results: Si True, retourne aussi les résultats bruts

        Returns:
            str ou Dict: La réponse générée
        """
        question_normalized = question.lower().strip()

        # Historique
        self.history.append({
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "mode": "llm" if self.llm_enabled else "rule-based"
        })

        # Si LLM n'est pas activé, utiliser le mode rule-based
        if not self.llm_enabled:
            response = self._answer_rule_based(question)
            result = {"response": response, "mode": "rule-based"}
            if return_tool_results:
                result["tool_results"] = []
            return result if return_tool_results else response

        # Mode LLM: décider des outils
        try:
            tools_to_call = self._call_llm_for_tools(question)

            if not tools_to_call:
                # Aucun outil choisi, utiliser le fallback
                response = self._answer_rule_based(question)
                result = {"response": response, "mode": "llm-fallback"}
                if return_tool_results:
                    result["tool_results"] = []
                return result if return_tool_results else response

            # Exécuter les outils
            tool_results = []
            for tool_call in tools_to_call:
                tool_name = tool_call.get("tool", "")
                arguments = tool_call.get("arguments", {})

                # Fuzzy match des colonnes
                if "column" in arguments:
                    matched = self._fuzzy_match_column(arguments["column"])
                    if matched:
                        arguments["column"] = matched
                if "column_x" in arguments:
                    matched = self._fuzzy_match_column(arguments["column_x"])
                    if matched:
                        arguments["column_x"] = matched
                if "column_y" in arguments:
                    matched = self._fuzzy_match_column(arguments["column_y"])
                    if matched:
                        arguments["column_y"] = matched

                # Exécuter
                result, success = self._execute_tool(tool_name, arguments)
                tool_results.append((tool_name, result, success))
                logger.info(f"Tool executed: {tool_name} -> {'success' if success else 'error'}")

            # Générer la réponse finale
            response = self._generate_response_from_tools(question, tool_results)

            result = {"response": response, "mode": "llm", "tool_results": tool_results}
            return result if return_tool_results else response

        except Exception as e:
            logger.error(f"Erreur QA: {e}, fallback")
            # Fallback complet
            response = self._answer_rule_based(question)
            result = {"response": response, "mode": "error-fallback", "error": str(e)}
            return result if return_tool_results else response

    def ask_multiple(self, questions: List[str]) -> List[Dict[str, Any]]:
        """
        Répond à plusieurs questions.

        Args:
            questions: Liste de questions

        Returns:
            List[Dict]: [{question, response, mode}]
        """
        results = []
        for q in questions:
            answer = self.answer(q, return_tool_results=True)
            if isinstance(answer, dict):
                results.append(answer)
            else:
                results.append({"question": q, "response": answer, "mode": "unknown"})
        return results

    def reset_history(self) -> None:
        """Réinitialise l'historique des questions."""
        self.history = []
        logger.info("Historique réinitialisé")

    def get_column_types(self) -> Dict[str, str]:
        """Retourne les types inférés des colonnes."""
        return self.column_types.copy()

    def get_context(self) -> Dict[str, Any]:
        """Retourne le contexte actuel."""
        return self.context.copy()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module de Questions/Réponses chargé.")
    print("Utilisez DataQA(df) pour interroger un DataFrame.")

    # Test simple
    print("\nTest:")
    df = pd.DataFrame({
        "nom": ["Alice", "Bob", "Charlie", "Alice"],
        "âge": [25, 30, 35, 25],
        "ville": ["Paris", "Lyon", "Paris", "Marseille"],
        "prix": [100, 150, 200, 120]
    })
    qa = DataQA(df)
    print(f"Colonnes: {qa.get_column_types()}")
    print(qa.answer("Combien de lignes?"))
    print(qa.answer("Statistiques de âge?"))
    print(qa.answer("Valeurs plus fréquentes de ville?"))
