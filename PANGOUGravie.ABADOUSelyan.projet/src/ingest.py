"""
Module de chargement des données (Ingestion).

Ce module fournit des fonctions pour charger des données depuis
différentes sources (CSV, Excel, bases de données, etc.) avec une
gestion robuste des erreurs et des métadonnées.
"""

import pandas as pd
import numpy as np
import logging
import re
from pathlib import Path
from typing import Optional, Union, Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Valeurs considérées comme manquantes
MISSING_VALUES = {"", "NA", "NaN", "null", "None", "-"}

# Taille seuil pour fichier volumineux (200 Mo)
LARGE_FILE_THRESHOLD = 200 * 1024 * 1024  # 200 MB
DEFAULT_MAX_ROWS = 200_000


class EmptyCSVError(Exception):
    """Exception levée lorsqu'un fichier CSV est vide."""
    pass


class IngestionWarning(Warning):
    """Avertissement lors de l'ingestion des données."""
    pass


def detect_separator(filepath: Union[str, Path], max_lines: int = 100) -> Tuple[str, int]:
    """
    Détecte le séparateur CSV en essayant plusieurs séparateurs.

    Essaie ',', ';', '\t', '|' et retourne celui qui donne le plus
    de colonnes cohérentes (nombre de lignes égales).

    Args:
        filepath: Chemin vers le fichier CSV
        max_lines: Nombre maximum de lignes à analyser

    Returns:
        Tuple: (séparateur détecté, nombre de colonnes)
    """
    filepath = Path(filepath)
    separators = [',', ';', '\t', '|']

    best_sep = ','
    best_cols = 0
    best_counts = {}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            line = line.strip()
            if not line:
                continue

            for sep in separators:
                parts = line.split(sep)
                count = len(parts)
                if sep not in best_counts:
                    best_counts[sep] = []
                best_counts[sep].append(count)

    # Trouver le séparateur qui donne le plus de colonnes cohérentes
    for sep in separators:
        if sep in best_counts:
            counts = best_counts[sep]
            # Le séparateur est bon si au moins 80% des lignes ont le même nombre de colonnes
            if counts:
                most_common = max(set(counts), key=counts.count)
                consistency = counts.count(most_common) / len(counts)
                if consistency >= 0.8 and most_common > best_cols:
                    best_cols = most_common
                    best_sep = sep

    logger.info(f"Séparateur détecté: '{best_sep}' ({best_cols} colonnes)")
    return best_sep, best_cols


def detect_encoding(filepath: Union[str, Path]) -> str:
    """
    Détecte l'encodage du fichier en essayant plusieurs encodings.

    Essaie utf-8, latin-1, cp1252.

    Args:
        filepath: Chemin vers le fichier

    Returns:
        str: L'encoding détecté
    """
    filepath = Path(filepath)
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                f.read(1024)  # Lire un petit échantillon
            logger.info(f"Encoding détecté: {encoding}")
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue

    logger.warning("Aucun encoding détecté, utilisation de latin-1 en fallback")
    return 'latin-1'


def normalize_column_name(col: str) -> str:
    """
    Normalise le nom d'une colonne.

    - Met en minuscules
    - Remplace les espaces par des underscores
    - Supprime les caractères spéciaux (sauf underscore)
    - Supprime les doubles underscores

    Args:
        col: Le nom de la colonne à normaliser

    Returns:
        str: Le nom normalisé
    """
    if not isinstance(col, str):
        col = str(col)

    # Minuscules
    col = col.lower()
    # Espaces -> underscores
    col = col.replace(' ', '_')
    # Supprimer les caractères spéciaux (garder alphanumérique et underscore)
    col = re.sub(r'[^a-z0-9_]', '', col)
    # Supprimer les underscores doubles
    col = re.sub(r'_+', '_', col)
    # Supprimer les underscores en début/fin
    col = col.strip('_')

    return col if col else 'column'


def load_csv(
    filepath: Union[str, Path],
    encoding: Optional[str] = None,
    separator: Optional[str] = None,
    skiprows: int = 0,
    dtype: Optional[Dict[str, Any]] = None,
    parse_dates: bool = False,
    max_rows: Optional[int] = None,
    **kwargs
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Charge un fichier CSV en un DataFrame pandas avec détection automatique.

    Args:
        filepath: Chemin vers le fichier CSV
        encoding: Encodage du fichier (None pour auto-detect)
        separator: Séparateur de champs (None pour auto-detect)
        skiprows: Nombre de lignes à ignorer au début (défaut: 0)
        dtype: Dictionnaire spécifiant les types des colonnes
        parse_dates: Booléen pour parser les dates (défaut: False)
        max_rows: Nombre maximum de lignes à charger (None pour toutes)
        **kwargs: Arguments supplémentaires passés à pd.read_csv()

    Returns:
        Tuple[pd.DataFrame, dict]: Les données chargées et les métadonnées d'ingestion

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        EmptyCSVError: Si le fichier est vide
        ValueError: Si le fichier est invalide
    """
    filepath = Path(filepath)
    ingestion_meta = {
        "filepath": str(filepath),
        "filename": filepath.name,
        "size_bytes": filepath.stat().st_size,
        "encoding_used": None,
        "separator_used": None,
        "rows_loaded": 0,
        "columns_loaded": 0,
        "warnings": [],
        "errors": [],
        "timestamp": datetime.now().isoformat()
    }

    # Vérifier si le fichier existe
    if not filepath.exists():
        error_msg = f"Fichier introuvable: {filepath}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Vérifier si le fichier est vide
    if filepath.stat().st_size == 0:
        error_msg = f"Fichier vide: {filepath}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise EmptyCSVError(error_msg)

    # Détection de l'encoding si non spécifié
    if encoding is None:
        encoding = detect_encoding(filepath)
    ingestion_meta["encoding_used"] = encoding

    # Détection du séparateur si non spécifié
    if separator is None:
        separator, _ = detect_separator(filepath)
    ingestion_meta["separator_used"] = separator

    # Avertissement pour fichier très gros
    if filepath.stat().st_size > LARGE_FILE_THRESHOLD:
        warning_msg = f"Fichier volumineux ({filepath.stat().st_size / (1024*1024):.1f} MB), chargement limité à {max_rows or DEFAULT_MAX_ROWS} lignes"
        ingestion_meta["warnings"].append(warning_msg)
        logger.warning(warning_msg)

    # Configuration des paramètres de lecture
    # Note: low_memory ne fonctionne pas avec engine='python', on utilise cParser
    read_params = {
        'encoding': encoding,
        'sep': separator,
        'skiprows': skiprows,
        'engine': 'c',  # 'c' engine supporte low_memory
        'on_bad_lines': 'skip',
        'low_memory': False,
        'na_values': MISSING_VALUES,
        'keep_default_na': True,
    }

    if max_rows:
        read_params['nrows'] = max_rows
    elif filepath.stat().st_size > LARGE_FILE_THRESHOLD:
        read_params['nrows'] = max_rows or DEFAULT_MAX_ROWS
        ingestion_meta["warnings"].append(f"Chargement limité à {read_params['nrows']} lignes pour fichier volumineux")

    read_params.update(kwargs)

    try:
        logger.info(f"Chargement du fichier CSV: {filepath}")
        df = pd.read_csv(filepath, **read_params)

        # Normaliser les noms de colonnes
        original_columns = list(df.columns)
        df.columns = [normalize_column_name(col) for col in df.columns]
        ingestion_meta["columns_original"] = original_columns
        ingestion_meta["columns_normalized"] = list(df.columns)

        # Vérifier si le fichier est petit
        if len(df) < 10:
            warning_msg = f"Fichier très petit: {len(df)} ligne(s), analyse limitée"
            ingestion_meta["warnings"].append(warning_msg)
            logger.warning(warning_msg)

        ingestion_meta["rows_loaded"] = len(df)
        ingestion_meta["columns_loaded"] = len(df.columns)

        logger.info(f"Fichier chargé: {len(df)} lignes, {len(df.columns)} colonnes")
        logger.info(f"Colonnes: {list(df.columns)}")

        return df, ingestion_meta

    except pd.errors.EmptyDataError:
        error_msg = f"Fichier CSV vide: {filepath}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise EmptyCSVError(error_msg)
    except pd.errors.ParserError as e:
        error_msg = f"Erreur de parsing CSV: {e}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise ValueError(error_msg)
    except UnicodeDecodeError as e:
        error_msg = f"Erreur d'encoding: {e}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Erreur inattendue lors du chargement: {e}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise


def load_excel(
    filepath: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    **kwargs
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Charge un fichier Excel en un DataFrame pandas.

    Args:
        filepath: Chemin vers le fichier Excel
        sheet_name: Nom ou index de la feuille à charger (défaut: 0)
        **kwargs: Arguments supplémentaires passés à pd.read_excel()

    Returns:
        Tuple[pd.DataFrame, dict]: Les données chargées et les métadonnées d'ingestion

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le fichier est invalide
    """
    filepath = Path(filepath)
    ingestion_meta = {
        "filepath": str(filepath),
        "filename": filepath.name,
        "size_bytes": filepath.stat().st_size,
        "sheet_used": sheet_name,
        "rows_loaded": 0,
        "columns_loaded": 0,
        "warnings": [],
        "errors": [],
        "timestamp": datetime.now().isoformat()
    }

    if not filepath.exists():
        error_msg = f"Fichier introuvable: {filepath}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        logger.info(f"Chargement du fichier Excel: {filepath}")
        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)

        # Normaliser les noms de colonnes
        original_columns = list(df.columns)
        df.columns = [normalize_column_name(col) for col in df.columns]
        ingestion_meta["columns_original"] = original_columns
        ingestion_meta["columns_normalized"] = list(df.columns)

        ingestion_meta["rows_loaded"] = len(df)
        ingestion_meta["columns_loaded"] = len(df.columns)

        logger.info(f"Fichier chargé: {len(df)} lignes, {len(df.columns)} colonnes")

        return df, ingestion_meta

    except ValueError as e:
        error_msg = f"Erreur de chargement Excel: {e}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Erreur inattendue lors du chargement: {e}"
        ingestion_meta["errors"].append(error_msg)
        logger.error(error_msg)
        raise


def load_data(
    filepath: Union[str, Path],
    source_type: Optional[str] = None,
    **kwargs
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Charge des données depuis un fichier en détectant automatiquement le type.

    Args:
        filepath: Chemin vers le fichier de données
        source_type: Type explicite de source ('csv', 'excel', None pour auto-detect)
        **kwargs: Arguments supplémentaires passés aux fonctions spécifiques

    Returns:
        Tuple[pd.DataFrame, dict]: Les données chargées et les métadonnées d'ingestion

    Raises:
        ValueError: Si le type de fichier n'est pas supporté
    """
    filepath = Path(filepath)
    extension = filepath.suffix.lower()

    if source_type is None:
        if extension == ".csv":
            source_type = "csv"
        elif extension in [".xlsx", ".xls"]:
            source_type = "excel"
        else:
            error_msg = f"Type de fichier non supporté: {extension}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    if source_type == "csv":
        return load_csv(filepath, **kwargs)
    elif source_type == "excel":
        return load_excel(filepath, **kwargs)
    else:
        error_msg = f"Type de source inconnu: {source_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)


def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Retourne des métadonnées sur un DataFrame.

    Args:
        df: Le DataFrame à analyser

    Returns:
        Dict: Dictionnaire contenant:
            - shape: (lignes, colonnes)
            - dtypes: Types de chaque colonne
            - missing_values: Comptage des valeurs manquantes
            - memory_usage: Usage mémoire
    """
    info = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().mean() * 100).to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum(),
        "duplicate_rows": df.duplicated().sum(),
        "timestamp": datetime.now().isoformat()
    }

    logger.info(f"Metadata générées pour DataFrame: {info['shape']}")
    return info


if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Exemple d'utilisation avec un fichier de test
    print("Module d'ingestion de données chargé.")
    print("Utilisez load_data() pour charger un fichier.")

    # Création d'un fichier de test si besoin
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            df, meta = load_data(filepath)
            print(f"\nFichier chargé: {filepath}")
            print(f"Shape: {df.shape}")
            print(f"Colonnes: {list(df.columns)}")
            print(f"Encoding: {meta['encoding_used']}")
            print(f"Séparateur: {meta['separator_used']}")
            if meta['warnings']:
                print(f"Warnings: {meta['warnings']}")
        except Exception as e:
            print(f"Erreur: {e}")
    else:
        print("\nFournir un fichier CSV en argument pour tester:")
        print("  python -m src.ingest data/exemple.csv")
