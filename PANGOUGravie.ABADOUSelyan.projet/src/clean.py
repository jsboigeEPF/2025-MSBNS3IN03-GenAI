"""
Module de nettoyage et préparation des données (Clean).

Ce module fournit des fonctions pour nettoyer, transformer et préparer
les données pour l'analyse, avec une approche robuste aux données
arbitraires et aux cas limites.
"""

import pandas as pd
import numpy as np
import logging
import re
from typing import Optional, Union, Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


def infer_numeric_type(series: pd.Series) -> Tuple[pd.Series, str, List[str]]:
    """
    Infère et convertit une colonne en type numérique.

    Gère:
    - Virgule décimale (12,5 -> 12.5)
    - Espaces dans les nombres (1 200 -> 1200)
    - Format français (1 200,50 -> 1200.50)
    - Format américain (1,200.50 -> 1200.50)

    Args:
        series: La série à convertir

    Returns:
        Tuple: (série convertie, type inferé, liste de warnings)
    """
    warnings = []
    original = series.copy()

    # Convertir en string pour traitement
    str_series = original.astype(str)

    # Pattern pour détecter les formats
    # Format français: chiffres, espace, virgule décimale
    # Format américain: chiffres, virgule milliers, point décimal

    def clean_numeric(val: str) -> float:
        """Nettoie une valeur numérique."""
        if pd.isna(val) or val.strip() == '' or val.strip().lower() in ['na', 'nan', 'null', 'none', '-', '']:
            return np.nan

        val = val.strip()

        # Gérer les parenthèses (négatif)
        if val.startswith('(') and val.endswith(')'):
            val = '-' + val[1:-1]

        # Supprimer les caractères de devise
        val = re.sub(r'[$€£¥]', '', val)

        # Déterminer le format
        has_space = ' ' in val
        has_comma = ',' in val
        has_dot = '.' in val

        # Compter les décimales potentiels
        comma_count = val.count(',')
        dot_count = val.count('.')

        try:
            if has_space and comma_count == 1 and dot_count == 0:
                # Format français: "1 200,50"
                val = val.replace(' ', '').replace(',', '.')
            elif has_space and comma_count == 0 and dot_count == 1:
                # Format avec espace millier: "1 200.50"
                val = val.replace(' ', '').replace('.', '')
            elif has_comma and dot_count == 0:
                # Format français: "12,5" ou "1 200,50"
                if has_space:
                    val = val.replace(' ', '').replace(',', '.')
                else:
                    val = val.replace(',', '.')
            elif dot_count == 1 and comma_count > 0:
                # Format américain: "1,200.50"
                val = val.replace(',', '')
            elif has_comma and dot_count == 0:
                # Juste une virgule: "12,5"
                val = val.replace(',', '.')
            else:
                val = val.replace(',', '').replace(' ', '')

            return float(val)
        except (ValueError, TypeError):
            return np.nan

    # Appliquer le nettoyage
    cleaned = str_series.apply(clean_numeric)

    # Detecter le type fin
    numeric_values = cleaned.dropna()
    if len(numeric_values) > 0:
        if (numeric_values % 1 == 0).all():
            return cleaned.astype('Int64'), 'integer', warnings
        else:
            return cleaned.astype('float64'), 'float', warnings

    return original, 'unknown', warnings


def infer_datetime_type(series: pd.Series) -> Tuple[pd.Series, str, List[str]]:
    """
    Infère et convertit une colonne en type datetime.

    Gère les formats multiples:
    - YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
    - Timestamps (entiers ou floats)
    - Formats avec heure

    Args:
        series: La série à convertir

    Returns:
        Tuple: (série convertie, type inferé, liste de warnings)
    """
    warnings = []
    original = series.copy()

    # Tenter plusieurs formats
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
    ]

    # Première tentative: pd.to_datetime avec inference
    try:
        converted = pd.to_datetime(original, errors='raise', dayfirst=True)
        if converted.notna().sum() > 0:
            return converted, 'datetime', warnings
    except Exception:
        pass

    # Tentative avec formats spécifiques
    for fmt in formats:
        try:
            converted = pd.to_datetime(original, format=fmt, errors='coerce')
            if converted.notna().sum() > 0:
                return converted, 'datetime', warnings
        except Exception:
            continue

    # Tentative avec timestamp (entiers)
    try:
        # Conversion en numeric d'abord
        numeric_series = pd.to_numeric(original, errors='coerce')
        # Si c'est un timestamp (grande valeur)
        if numeric_series.notna().any():
            max_val = numeric_series.max()
            min_val = numeric_series.min()
            # Timestamp typique: > 1e9 (années 2000+)
            if max_val > 1e9 or (min_val > 1e9 and max_val < 2e9):
                converted = pd.to_datetime(numeric_series, unit='s', errors='coerce')
                if converted.notna().sum() > 0:
                    return converted, 'timestamp', warnings
    except Exception:
        pass

    return original, 'unknown', warnings


def infer_column_types(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Infère le type de chaque colonne.

    Types: 'numeric', 'datetime', 'categorical', 'unknown'

    Args:
        df: Le DataFrame à analyser

    Returns:
        Dict: {col_name: {'type': str, 'converted': bool, 'original_dtype': str, 'warnings': List}}
    """
    type_inference = {}

    for col in df.columns:
        original_dtype = str(df[col].dtype)
        series = df[col]

        result = {
            'type': 'unknown',
            'converted': False,
            'original_dtype': original_dtype,
            'warnings': []
        }

        # Essayer numeric d'abord
        numeric_data, num_type, num_warnings = infer_numeric_type(series)
        if num_type in ['integer', 'float']:
            result['type'] = 'numeric'
            result['converted'] = True
            result['warnings'] = num_warnings
            type_inference[col] = result
            continue

        # Essayer datetime
        datetime_data, dt_type, dt_warnings = infer_datetime_type(series)
        if dt_type in ['datetime', 'timestamp']:
            result['type'] = 'datetime'
            result['converted'] = True
            result['warnings'] = dt_warnings
            type_inference[col] = result
            continue

        # Catégorielle par défaut (texte ou code)
        result['type'] = 'categorical'
        type_inference[col] = result

    logger.info(f"Types inferes: {len(type_inference)} colonnes")
    return type_inference


def handle_missing_values_smart(
    df: pd.DataFrame,
    type_inference: Optional[Dict[str, Dict[str, Any]]] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Gère les valeurs manquantes intelligemment selon le type de colonne.

    - Numérique -> médiane
    - Catégorielle -> mode
    - Date -> NaT (conservé comme manquant)

    Args:
        df: Le DataFrame à nettoyer
        type_inference: Résultat de infer_column_types (None pour auto)

    Returns:
        Tuple: (df nettoyé, résumé des NA avant/après)
    """
    df_clean = df.copy()
    missing_summary = {
        'before': {},
        'after': {},
        'strategy': {}
    }

    # Infer les types si non fournis
    if type_inference is None:
        type_inference = infer_column_types(df_clean)

    # Premier passage: compter les NA avant
    for col in df_clean.columns:
        missing_summary['before'][col] = int(df_clean[col].isnull().sum())

    # Deuxième passage: gérer les NA selon le type
    for col in df_clean.columns:
        col_info = type_inference.get(col, {})
        col_type = col_info.get('type', 'categorical')

        if col_type == 'numeric':
            # S'assurer que la colonne est bien numérique
            series = df_clean[col]
            if pd.api.types.is_numeric_dtype(series):
                median_val = series.median()
                if pd.isna(median_val) and series.notna().any():
                    median_val = 0
                df_clean[col] = series.fillna(median_val)
                missing_summary['strategy'][col] = f'median ({median_val})'
            else:
                # Tenter la conversion
                converted, _, _ = infer_numeric_type(series)
                if pd.api.types.is_numeric_dtype(converted):
                    median_val = converted.median()
                    df_clean[col] = converted.fillna(median_val)
                    missing_summary['strategy'][col] = f'median ({median_val}) (converti)'
                else:
                    missing_summary['strategy'][col] = 'pas de remplacement (non numérique)'
                    logger.warning(f"Colonne {col}: impossible de calculer la médiane")

        elif col_type == 'categorical':
            series = df_clean[col]
            if series.notna().any():
                mode_val = series.mode()
                fill_val = mode_val.iloc[0] if len(mode_val) > 0 else 'Unknown'
            else:
                fill_val = 'Unknown'
            df_clean[col] = series.fillna(fill_val)
            missing_summary['strategy'][col] = f'mode ({fill_val})'

        elif col_type == 'datetime':
            # Garder les NaT (NaN pour datetime)
            missing_summary['strategy'][col] = 'NaT (conservé)'

        # Compter les NA après
        missing_summary['after'][col] = int(df_clean[col].isnull().sum())

    logger.info(f"Valeurs manquantes gérées: {len(type_inference)} colonnes")
    return df_clean, missing_summary


def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Tuple[pd.DataFrame, int]:
    """
    Supprime les lignes dupliquées.

    Args:
        df: Le DataFrame
        subset: Colonnes à considérer pour les doublons (None = toutes)

    Returns:
        Tuple: (df sans doublons, nombre de doublons supprimés)
    """
    before_count = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    duplicates_removed = before_count - len(df_clean)

    logger.info(f"Doublons supprimés: {duplicates_removed} lignes")
    return df_clean, duplicates_removed


def normalize_text_strings(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Normalise les colonnes de type string.

    - strip()
    - convertir "" -> NA
    - normaliser les espaces

    Args:
        df: Le DataFrame
        columns: Colonnes à normaliser

    Returns:
        Tuple: (df normalisé, nombre de changements par colonne)
    """
    df_norm = df.copy()
    changes = {}

    if columns is None:
        columns = df_norm.select_dtypes(include=['object', 'string']).columns.tolist()

    for col in columns:
        before_empty = (df_norm[col].astype(str).str.strip() == '').sum()
        before_total = df_norm[col].notna().sum()

        # Convertir en string, strip, et remplacer les chaînes vides par NA
        df_norm[col] = df_norm[col].astype(str).str.strip()
        df_norm[col] = df_norm[col].replace({'': pd.NA})
        # Remplacer les chaînes vides (après replace) par NA
        df_norm[col] = df_norm[col].replace({'': np.nan})

        # Normaliser les espaces multiples
        df_norm[col] = df_norm[col].astype(str).str.replace(r'\s+', ' ', regex=True)

        after_empty = (df_norm[col].isna()).sum()
        changes[col] = int(after_empty - before_empty) if after_empty > before_empty else 0

    logger.info(f"Strings normalisés: {len(columns)} colonnes")
    return df_norm, changes


def detect_outliers_iqr(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    threshold: float = 1.5
) -> Dict[str, Dict[str, Any]]:
    """
    Détecte les outliers avec la méthode IQR.

    Args:
        df: Le DataFrame
        columns: Colonnes à analyser (None = toutes numériques)
        threshold: Multiplicateur IQR (défaut: 1.5)

    Returns:
        Dict: {col: {lower, upper, count, percentage, iqr}}
    """
    outlier_stats = {}

    numeric_cols = columns if columns else df.select_dtypes(include=[np.number]).columns.tolist()

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 3:
            continue

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outliers_mask.sum()
        outlier_percentage = (outlier_count / len(df)) * 100

        outlier_stats[col] = {
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'count': int(outlier_count),
            'percentage': float(outlier_percentage),
            'iqr': float(IQR)
        }

    logger.info(f"Outliers détectés: {len(outlier_stats)} colonnes")
    return outlier_stats


def winsorize_outliers(
    df: pd.DataFrame,
    outlier_stats: Dict[str, Dict[str, Any]],
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Winsorize les outliers (clip aux bornes IQR).

    Args:
        df: Le DataFrame
        outlier_stats: Résultat de detect_outliers_iqr
        columns: Colonnes à traiter

    Returns:
        pd.DataFrame: DataFrame avec outliers winsorizés
    """
    df_clean = df.copy()

    target_cols = columns if columns else list(outlier_stats.keys())

    for col in target_cols:
        if col not in df_clean.columns:
            continue

        stats = outlier_stats.get(col, {})
        lower = stats.get('lower_bound', df_clean[col].min())
        upper = stats.get('upper_bound', df_clean[col].max())

        df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)

    logger.info(f"Outliers winsorizés: {len(target_cols)} colonnes")
    return df_clean


def clean_data(
    df: pd.DataFrame,
    handle_duplicates: bool = True,
    handle_outliers: bool = True,
    winsorize: bool = False,
    normalize_strings: bool = True,
    infer_types: bool = True,
    **kwargs
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Fonction principale pour nettoyer un DataFrame.

    Pipeline complet:
    1. Inférence de types
    2. Gestion des NA (médiane/mode)
    3. Suppression des doublons
    4. Normalisation des strings
    5. Détection/outliers (IQR)

    Args:
        df: Le DataFrame à nettoyer
        handle_duplicates: Supprimer les doublons
        handle_outliers: Détecter les outliers
        winsorize: Winsorize les outliers au lieu de les supprimer
        normalize_strings: Normaliser les colonnes string
        infer_types: Inférer les types de colonnes

    Returns:
        Tuple: (df_clean, data_quality_summary)
    """
    logger.info("Début du nettoyage des données")
    logger.info(f"Shape initiale: {df.shape}")

    data_quality_summary = {
        'before': {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_bytes': int(df.memory_usage(deep=True).sum()),
            'na_count': int(df.isnull().sum().sum()),
            'duplicates': int(df.duplicated().sum())
        },
        'after': {},
        'warnings': [],
        'type_inference': {},
        'missing_values': {},
        'duplicates_removed': 0,
        'outliers_detected': {}
    }

    # Etape 1: Inférence de types
    if infer_types:
        type_inference = infer_column_types(df)
        data_quality_summary['type_inference'] = type_inference
        logger.info("Inférence de types complétée")

    # Etape 2: Gestion des valeurs manquantes
    df_clean, missing_summary = handle_missing_values_smart(df, type_inference if infer_types else None)
    data_quality_summary['missing_values'] = missing_summary

    # Etape 3: Suppression des doublons
    if handle_duplicates:
        df_clean, dup_removed = remove_duplicates(df_clean)
        data_quality_summary['duplicates_removed'] = dup_removed
        if dup_removed > 0:
            data_quality_summary['warnings'].append(f"{dup_removed} lignes dupliquées supprimées")

    # Etape 4: Normalisation des strings
    if normalize_strings:
        df_clean, str_changes = normalize_text_strings(df_clean)
        if any(str_changes.values()):
            data_quality_summary['warnings'].append("Strings normalisés")
        logger.info("Normalisation des strings complétée")

    # Etape 5: Gestion des outliers
    if handle_outliers:
        outlier_stats = detect_outliers_iqr(df_clean)
        data_quality_summary['outliers_detected'] = outlier_stats

        if winsorize:
            df_clean = winsorize_outliers(df_clean, outlier_stats)
            data_quality_summary['warnings'].append("Outliers winsorizés")
        else:
            # Marquer les outliers dans le résumé
            for col, stats in outlier_stats.items():
                if stats['count'] > 0:
                    data_quality_summary['warnings'].append(
                        f"{col}: {stats['count']} outliers ({stats['percentage']:.1f}%)"
                    )

    # Finalisation
    data_quality_summary['after'] = {
        'rows': len(df_clean),
        'columns': len(df_clean.columns),
        'memory_bytes': int(df_clean.memory_usage(deep=True).sum()),
        'na_count': int(df_clean.isnull().sum().sum()),
        'duplicates': int(df_clean.duplicated().sum())
    }

    logger.info(f"Nettoyage termine: {df_clean.shape}")

    return df_clean, data_quality_summary


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module de nettoyage de données chargé.")
    print("Utilisez clean_data(df) pour nettoyer un DataFrame.")
