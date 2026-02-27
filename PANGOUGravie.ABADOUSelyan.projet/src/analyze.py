"""
Module d'analyse statistique et exploration (Analyze).

Ce module fournit des fonctions pour explorer, analyser et obtenir
des statistiques descriptives sur des jeux de données, avec une
approche robuste aux données arbitraires et une intégration LLM.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

from src.config_env import is_llm_enabled as llm_enabled
from src.llm import run_llm_json, LLMError

logger = logging.getLogger(__name__)

# Configuration par défaut pour les analyses
DEFAULT_TOP_N_CATEGORIES = 5
DEFAULT_CORRELATION_THRESHOLD = 0.7


def get_data_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Génère un profil complet du DataFrame.

    Args:
        df: Le DataFrame à profiler

    Returns:
        Dict: Profil contenant shape, dtypes, missingness, etc.
    """
    profile = {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "memory_bytes": int(df.memory_usage(deep=True).sum()),
        "missingness": {
            "total_na": int(df.isnull().sum().sum()),
            "percentage_na": float(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
            if len(df) > 0 and len(df.columns) > 0 else 0.0
        },
        "column_types": {},
        "cardinalities": {},
        "sample": {}
    }

    # Profil par colonne
    for col in df.columns:
        series = df[col]
        col_type = "unknown"
        col_dtype = str(series.dtype)

        if pd.api.types.is_numeric_dtype(series):
            col_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            col_type = "datetime"
        else:
            col_type = "categorical"

        profile["column_types"][col] = {
            "type": col_type,
            "dtype": col_dtype,
            "count": int(series.count()),
            "missing_count": int(series.isnull().sum()),
            "missing_pct": float(series.isnull().mean() * 100) if len(series) > 0 else 0.0
        }

        # Cardinalité pour catégorielles
        if col_type == "categorical":
            unique_count = int(series.nunique(dropna=False)) if len(series) > 0 else 0
            unique_pct = float(unique_count / len(series) * 100) if len(series) > 0 else 0.0

            # IMPORTANT: on fournit "unique_count" (et on garde "unique" pour compat)
            profile["cardinalities"][col] = {
                "unique_count": unique_count,
                "unique_pct": unique_pct,
                "unique": unique_count  # compat avec anciens appels
            }

    # Échantillon (max 5 lignes, strings tronqués à 50 chars)
    sample_size = min(5, len(df))
    sample_df = df.iloc[:sample_size].copy()

    for col in sample_df.columns:
        if sample_df[col].dtype == "object" or str(sample_df[col].dtype).startswith("string"):
            sample_df[col] = sample_df[col].astype(str).str.slice(0, 50)

    profile["sample"] = sample_df.to_dict(orient="records")

    return profile


def describe_numeric(df: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Génère des statistiques descriptives pour les colonnes numériques.
    """
    numeric_cols = columns if columns else df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return {}

    describe_df = df[numeric_cols].describe()
    stats: Dict[str, Any] = {}

    for col in numeric_cols:
        mean_val = describe_df.loc["mean", col]
        std_val = describe_df.loc["std", col]
        skew_val = df[col].skew()
        kurt_val = df[col].kurt()

        col_stats = {
            "count": int(describe_df.loc["count", col]),
            "mean": float(mean_val) if not pd.isna(mean_val) else None,
            "std": float(std_val) if not pd.isna(std_val) else None,
            "min": float(describe_df.loc["min", col]) if not pd.isna(describe_df.loc["min", col]) else None,
            "max": float(describe_df.loc["max", col]) if not pd.isna(describe_df.loc["max", col]) else None,
            "median": float(df[col].median()) if not pd.isna(df[col].median()) else None,
            "skewness": float(skew_val) if not pd.isna(skew_val) else None,
            "kurtosis": float(kurt_val) if not pd.isna(kurt_val) else None
        }
        stats[col] = col_stats

    logger.info(f"Stats numériques: {len(stats)} colonnes")
    return stats


def describe_categorical(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    top_n: int = DEFAULT_TOP_N_CATEGORIES
) -> Dict[str, Any]:
    """
    Génère des statistiques pour les colonnes catégorielles.
    """
    categorical_cols = columns if columns else df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not categorical_cols:
        return {}

    stats: Dict[str, Any] = {}
    for col in categorical_cols:
        value_counts = df[col].value_counts(dropna=False)

        top_values = []
        for val, count in value_counts.head(top_n).items():
            top_values.append({
                "value": str(val) if val is not None else "null",
                "count": int(count),
                "percentage": float(count / len(df) * 100) if len(df) > 0 else 0.0
            })

        stats[col] = {
            "top_values": top_values,
            "unique_count": int(df[col].nunique(dropna=False)) if len(df) > 0 else 0,
            "missing_count": int(df[col].isnull().sum()) if len(df) > 0 else 0,
            "most_frequent": top_values[0] if top_values else None
        }

    logger.info(f"Stats catégorielles: {len(stats)} colonnes")
    return stats


def analyze_dates(df: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Analyse les colonnes de dates.
    """
    date_cols = columns if columns else df.select_dtypes(
        include=["datetime64", "datetime64[ns]", "datetime64[ns, UTC]"]
    ).columns.tolist()

    if not date_cols:
        return {}

    stats: Dict[str, Any] = {}
    for col in date_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        min_date = series.min()
        max_date = series.max()
        range_days = (max_date - min_date).days

        try:
            month_counts = series.dt.month.value_counts()
            has_month_pattern = len(month_counts) >= 4
        except Exception:
            has_month_pattern = False

        stats[col] = {
            "min": str(min_date),
            "max": str(max_date),
            "range_days": int(range_days),
            "count": int(len(series)),
            "has_month_pattern": has_month_pattern,
            "sample_values": [str(v) for v in series.head(3).tolist()]
        }

    logger.info(f"Analyse dates: {len(stats)} colonnes")
    return stats


def calculate_correlations(
    df: pd.DataFrame,
    threshold: float = DEFAULT_CORRELATION_THRESHOLD
) -> Tuple[Optional[pd.DataFrame], List[Dict[str, Any]]]:
    """
    Calcule les corrélations et trouve les paires fortes.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) < 2:
        return None, []

    corr_matrix = df[numeric_cols].corr(method="pearson")
    strong_correlations: List[Dict[str, Any]] = []

    for i, col1 in enumerate(corr_matrix.columns):
        for col2 in corr_matrix.columns[i + 1:]:
            corr = corr_matrix.loc[col1, col2]
            if pd.notna(corr) and abs(corr) >= threshold:
                strong_correlations.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation": float(corr),
                    "strength": "strong" if abs(corr) >= 0.8 else "moderate"
                })

    logger.info(f"Corrélations: {len(strong_correlations)} paires fortes")
    return corr_matrix, strong_correlations


def generate_insights_basic(df: pd.DataFrame, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Génère des insights basiques (rule-based).
    """
    insights: List[Dict[str, Any]] = []

    # Insight 1: Taille du dataset
    rows = profile["shape"]["rows"]
    if rows < 100:
        insights.append({
            "type": "data_size",
            "severity": "low",
            "title": "Dataset de petite taille",
            "description": f"Le dataset contient seulement {rows} lignes. Les analyses statistiques peuvent être limitées.",
            "recommendation": "Considérez collecter plus de données ou utiliser des techniques d'analyse adaptées aux petits échantillons."
        })
    elif rows < 1000:
        insights.append({
            "type": "data_size",
            "severity": "info",
            "title": "Dataset de taille moyenne",
            "description": f"Le dataset contient {rows} lignes, suffisant pour des analyses statistiques de base."
        })

    # Insight 2: Données manquantes
    na_pct = profile["missingness"]["percentage_na"]
    if na_pct > 10:
        insights.append({
            "type": "missing_data",
            "severity": "high",
            "title": "Taux de valeurs manquantes élevé",
            "description": f"{na_pct:.1f}% des valeurs sont manquantes.",
            "recommendation": "Analyser les colonnes avec le plus de missing et décider de la stratégie de traitement."
        })
    elif na_pct > 0:
        insights.append({
            "type": "missing_data",
            "severity": "info",
            "title": "Présence de valeurs manquantes",
            "description": f"{na_pct:.1f}% des valeurs sont manquantes. Vérifier si le pattern est aléatoire."
        })

    # Insight 3: Colonnes à forte cardinalité
    cardinalities = profile.get("cardinalities", {})
    for col, card_info in cardinalities.items():
        if card_info.get("unique_pct", 0) > 90:
            unique_count = card_info.get("unique_count", card_info.get("unique", "plusieurs"))
            insights.append({
                "type": "high_cardinality",
                "severity": "info",
                "title": f"Colonne {col} très unique",
                "description": (
                    f"La colonne {col} a {unique_count} valeurs uniques sur "
                    f"{profile['shape']['rows']} lignes ({card_info.get('unique_pct', 0):.1f}%)."
                )
            })

    # Insight 4: Duplicates
    dup_count = int(df.duplicated().sum()) if df is not None else 0
    if dup_count > 0:
        insights.append({
            "type": "duplicates",
            "severity": "medium",
            "title": "Lignes dupliquées détectées",
            "description": f"{dup_count} lignes sont exactement doublées dans le dataset."
        })

    return insights


def generate_viz_suggestions_basic(
    profile: Dict[str, Any],
    correlations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Génère des suggestions de visualisation (rule-based).
    """
    suggestions: List[Dict[str, Any]] = []
    col_types = profile.get("column_types", {})

    # Histogramme pour chaque colonne numérique
    for col, info in col_types.items():
        if info.get("type") == "numeric":
            suggestions.append({
                "type": "histogram",
                "title": f"Distribution de {col}",
                "description": f"Histogramme montrant la distribution des valeurs de {col}",
                "column": col
            })

    # Boxplot pour colonnes numériques
    for col, info in col_types.items():
        if info.get("type") == "numeric":
            suggestions.append({
                "type": "boxplot",
                "title": f"Boxplot de {col}",
                "description": f"Boxplot pour détecter les outliers dans {col}",
                "column": col
            })

    # Scatter plot pour paires corrélées
    for corr in correlations[:3]:
        suggestions.append({
            "type": "scatter",
            "title": f"{corr['col1']} vs {corr['col2']}",
            "description": f"Scatter plot avec corrélation de {corr['correlation']:.2f}",
            "columns": [corr["col1"], corr["col2"]]
        })

    # Bar chart pour colonnes catégorielles avec peu de valeurs
    cardinalities = profile.get("cardinalities", {})
    for col, info in cardinalities.items():
        # IMPORTANT: on lit unique_count avec fallback sur unique
        uc = info.get("unique_count", info.get("unique", 0))
        try:
            uc_int = int(uc)
        except Exception:
            uc_int = 0

        if uc_int <= 10:
            suggestions.append({
                "type": "bar",
                "title": f"Répartition de {col}",
                "description": f"Bar chart montrant la répartition des catégories de {col}",
                "column": col
            })

    return suggestions


def generate_insights_llm(
    profile: Dict[str, Any],
    df_sample: pd.DataFrame,
    df_clean: pd.DataFrame,
    llm_config: Optional[Dict[str, Any]] = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Génère des insights avec LLM.
    """
    # Formatter le contexte pour le LLM
    context = f"""
Dataset: {profile['shape']['rows']} lignes, {profile['shape']['columns']} colonnes
Types de colonnes: {profile['column_types']}
Missingness: {profile['missingness']}

Échantillon (5 lignes max):
{df_sample.to_string(index=False)}
"""

    system_prompt = """Tu es un analyste de données expert. Analyse ce dataset et fournis:

1. 8-12 insights actionnables (max 1 phrase chacun)
2. 3 hypothèses/pistes à explorer
3. 5 suggestions de visualisations spécifiques

Format JSON:
{
  "insights": [{"title": str, "description": str, "impact": "high/medium/low"}],
  "hypotheses": [{"title": str, "description": str, "validation": str}],
  "visualizations": [{"type": str, "columns": list, "purpose": str}]
}

Règles:
- Ne jamais inclure de code Python
- Fournir des insights concis et actionnables
- Les visualisations doivent être spécifiques (type, colonnes, objectif)
"""

    try:
        # IMPORTANT: utiliser llm_config si fourni (sinon enabled True minimal)
        cfg = llm_config if llm_config is not None else {"llm": {"enabled": True}}
        response = run_llm_json(cfg, system_prompt, context)

        # fallback minimal si champs manquants
        insights = response.get("insights") or generate_insights_basic(df_clean, profile)[:3]
        hypotheses = response.get("hypotheses") or [
            {"title": "Corrélation numérique", "description": "Certaines variables numériques sont corrélées", "validation": "Calculer la matrice de corrélation"}
        ]
        viz_suggestions = response.get("visualizations") or []

        return insights, hypotheses, viz_suggestions

    except (LLMError, ValueError) as e:
        logger.warning(f"LLM échoué, fallback: {e}")
        return (
            generate_insights_basic(df_clean, profile)[:5],
            [{"title": "Corrélation", "description": "Analyser les corrélations entre variables", "validation": "Calculer corrélations"}],
            generate_viz_suggestions_basic(profile, [])
        )


def analyze_data(
    df: pd.DataFrame,
    llm_config: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Fonction principale pour analyser un DataFrame.
    """
    logger.info("Début de l'analyse des données")
    logger.info(f"Shape du DataFrame: {df.shape}")

    profile = get_data_profile(df)

    numeric_stats = describe_numeric(df)
    categorical_stats = describe_categorical(df)
    date_stats = analyze_dates(df)
    corr_matrix, strong_correlations = calculate_correlations(df)

    # Préparer l'échantillon pour LLM (strings tronqués)
    df_sample = df.head(5).copy()
    for col in df_sample.select_dtypes(include=["object"]).columns:
        df_sample[col] = df_sample[col].astype(str).str.slice(0, 50)

    llm_enabled_flag = llm_enabled(llm_config) if llm_config else False

    if llm_enabled_flag:
        logger.info("Génération d'insights avec LLM")
        # IMPORTANT: passer df_sample DataFrame (pas dict)
        insights, hypotheses, viz_suggestions = generate_insights_llm(
            profile, df_sample, df, llm_config=llm_config
        )
    else:
        logger.info("Génération d'insights rule-based")
        insights = generate_insights_basic(df, profile)
        hypotheses = [{
            "title": "Corrélation",
            "description": "Analyser les corrélations entre variables",
            "validation": "Calculer corrélations"
        }]
        viz_suggestions = generate_viz_suggestions_basic(profile, strong_correlations)

    analysis_summary = {
        "shape": profile["shape"],
        "memory_bytes": profile["memory_bytes"],
        "column_types": profile["column_types"],
        "cardinalities": profile.get("cardinalities", {}),
        "missingness": profile["missingness"],
        "numeric_stats": numeric_stats,
        "categorical_stats": categorical_stats,
        "date_stats": date_stats,
        "correlations": {
            "matrix": corr_matrix.to_dict() if corr_matrix is not None else {},
            "strong_correlations": strong_correlations
        },
        "insights": insights,
        "hypotheses": hypotheses,
        "viz_suggestions": viz_suggestions,
        "timestamp": datetime.now().isoformat()
    }

    logger.info(f"Analyse complétée: {len(insights)} insights, {len(viz_suggestions)} visualisations suggérées")
    return analysis_summary, insights, viz_suggestions


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module d'analyse de données chargé.")
    print("Utilisez analyze_data(df) pour analyser un DataFrame.")