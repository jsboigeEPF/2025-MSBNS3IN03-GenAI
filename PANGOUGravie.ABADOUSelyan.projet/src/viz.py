"""
Module de visualisation des données (Viz).

Ce module fournit des fonctions pour créer des visualisations
statistiques avec matplotlib, y compris des histogrammes,
boxplots, scatter plots, et des visualisations de séries temporelles.
Supporte la génération dynamique selon les types de colonnes.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Mode sans affichage pour les environnements headless
import matplotlib.pyplot as plt
import logging
from typing import Optional, Union, Dict, Any, List, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Répertoire par défaut pour les figures
DEFAULT_FIGURES_DIR = "outputs/figures"


def setup_visualization(style: str = "default") -> None:
    """
    Configure les paramètres de visualisation.

    Args:
        style: Style de visualisation ('default', 'dark', 'publication')
    """
    if style == "default":
        plt.style.use("default")
    elif style == "dark":
        plt.style.use("dark_background")
    elif style == "publication":
        plt.style.use("seaborn-v0_8-whitegrid")
        plt.rcParams.update({
            "font.size": 12,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.dpi": 300
        })

    logger.info(f"Style de visualisation: {style}")


def create_histogram(
    df: pd.DataFrame,
    column: str,
    output_path: Optional[Union[str, Path]] = None,
    bins: int = 30,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> Optional[plt.Figure]:
    """
    Crée un histogramme pour une colonne numérique.

    Returns None si la colonne n'est pas disponible ou non numérique.
    """
    if column not in df.columns:
        logger.warning(f"Colonne '{column}' introuvable pour histogramme")
        return None

    if not pd.api.types.is_numeric_dtype(df[column]):
        logger.warning(f"Colonne '{column}' n'est pas numérique (ignore histogramme)")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)
        data = df[column].dropna()

        if len(data) == 0:
            logger.warning(f"Colonne '{column}' vide pour histogramme")
            plt.close(fig)
            return None

        ax.hist(data, bins=bins, alpha=0.7, color="steelblue", edgecolor="black")
        ax.set_xlabel(column)
        ax.set_ylabel("Fréquence")
        ax.set_title(title or f"Distribution de {column}")
        ax.grid(True, alpha=0.3)

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Histogramme sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur histogramme {column}: {e}")
        return None


def create_boxplot(
    df: pd.DataFrame,
    column: str,
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> Optional[plt.Figure]:
    """
    Crée un boxplot pour une colonne numérique.

    Returns None si la colonne n'est pas disponible ou non numérique.
    """
    if column not in df.columns:
        logger.warning(f"Colonne '{column}' introuvable pour boxplot")
        return None

    if not pd.api.types.is_numeric_dtype(df[column]):
        logger.warning(f"Colonne '{column}' n'est pas numérique (ignore boxplot)")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)
        data = df[column].dropna()

        if len(data) == 0:
            logger.warning(f"Colonne '{column}' vide pour boxplot")
            plt.close(fig)
            return None

        ax.boxplot(data, vert=True, patch_artist=True,
                   boxprops=dict(facecolor="steelblue", alpha=0.7))
        ax.set_ylabel(column)
        ax.set_title(title or f"Boxplot de {column}")
        ax.grid(True, alpha=0.3, axis="y")

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Boxplot sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur boxplot {column}: {e}")
        return None


def create_bar_chart(
    df: pd.DataFrame,
    category_column: str,
    value_column: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None,
    top_n: int = 10,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> Optional[plt.Figure]:
    """
    Crée un bar chart pour une variable catégorielle.

    Returns None si la colonne n'est pas disponible.
    """
    if category_column not in df.columns:
        logger.warning(f"Colonne '{category_column}' introuvable pour bar chart")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)

        if value_column:
            if value_column not in df.columns:
                logger.warning(f"Colonne '{value_column}' introuvable pour aggregation")
                return None
            aggregated = df.groupby(category_column)[value_column].sum().nlargest(top_n)
            x = aggregated.index.astype(str)
            y = aggregated.values
            ax.bar(x, y, color="steelblue", alpha=0.7)
            ax.set_ylabel(value_column)
        else:
            counts = df[category_column].value_counts(dropna=False).nlargest(top_n)
            if len(counts) == 0:
                logger.warning(f"Colonne '{category_column}' sans valeurs valides")
                plt.close(fig)
                return None
            x = counts.index.astype(str)
            y = counts.values
            ax.bar(x, y, color="steelblue", alpha=0.7)
            ax.set_ylabel("Comptage")

        ax.set_xlabel(category_column)
        ax.set_title(title or f"Répartition de {category_column}")
        ax.grid(True, alpha=0.3, axis="y")
        plt.xticks(rotation=45, ha="right")

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Bar chart sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur bar chart {category_column}: {e}")
        return None


def create_time_series_plot(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    rolling_window: Optional[int] = None
) -> Optional[plt.Figure]:
    """
    Crée un graphique de série temporelle.

    Returns None si les colonnes ne sont pas disponibles ou ne peuvent pas être converties.
    """
    if date_column not in df.columns or value_column not in df.columns:
        logger.warning(f"Colonne(s) introuvable(s) pour time series")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)

        plot_df = df[[date_column, value_column]].copy()
        plot_df = plot_df.dropna(subset=[date_column, value_column])

        if len(plot_df) < 2:
            logger.warning(f"Pas assez de données pour time series: {date_column}, {value_column}")
            plt.close(fig)
            return None

        # Convertir en datetime si nécessaire
        if not pd.api.types.is_datetime64_any_dtype(plot_df[date_column]):
            plot_df[date_column] = pd.to_datetime(plot_df[date_column], errors='coerce')
            plot_df = plot_df.dropna(subset=[date_column])

        if len(plot_df) < 2:
            logger.warning(f"Conversion datetime échouée pour: {date_column}")
            plt.close(fig)
            return None

        plot_df = plot_df.sort_values(date_column)
        ax.plot(plot_df[date_column], plot_df[value_column],
                label=value_column, color="steelblue", linewidth=1)

        # Ajouter moyenne mobile si demandée
        if rolling_window:
            ma = plot_df[value_column].rolling(window=rolling_window).mean()
            ax.plot(plot_df[date_column], ma,
                    label=f"MA{rolling_window}", color="red", linewidth=2)

        ax.set_xlabel(date_column)
        ax.set_ylabel(value_column)
        ax.set_title(title or f"Série temporelle de {value_column}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Time series plot sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur time series {date_column}/{value_column}: {e}")
        return None


def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    output_path: Optional[Union[str, Path]] = None,
    title: str = "Matrice de corrélation",
    figsize: Tuple[int, int] = (10, 8)
) -> Optional[plt.Figure]:
    """
    Crée un heatmap de corrélation.

    Returns None si la matrice est vide ou invalide.
    """
    if corr_matrix is None or corr_matrix.empty:
        logger.warning("Matrice de corrélation vide")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)

        # S'assurer que c'est un DataFrame numérique
        try:
            corr_values = corr_matrix.values.flatten()
            if not all(isinstance(v, (int, float, np.number)) for v in corr_values):
                corr_matrix = corr_matrix.astype(float)
        except Exception:
            logger.warning("Matrice de corrélation non convertible en numérique")
            plt.close(fig)
            return None

        im = ax.imshow(corr_matrix.values, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)

        # Labels
        ax.set_xticks(np.arange(len(corr_matrix.columns)))
        ax.set_yticks(np.arange(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr_matrix.columns)

        # Texte avec les valeurs
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                val = corr_matrix.iloc[i, j]
                if pd.isna(val):
                    continue
                text = ax.text(j, i, f"{val:.2f}",
                              ha="center", va="center", color="white", fontsize=8)

        plt.colorbar(im, ax=ax, label="Corrélation")
        ax.set_title(title)

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Heatmap sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur heatmap: {e}")
        return None


def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> Optional[plt.Figure]:
    """
    Crée un scatter plot pour deux colonnes numériques.

    Returns None si les colonnes ne sont pas disponibles ou non numériques.
    """
    if x_column not in df.columns or y_column not in df.columns:
        logger.warning(f"Colonne(s) introuvable(s) pour scatter plot: {x_column}, {y_column}")
        return None

    if not pd.api.types.is_numeric_dtype(df[x_column]) or not pd.api.types.is_numeric_dtype(df[y_column]):
        logger.warning(f"Colonne(s) non numérique(s) pour scatter plot")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)
        data = df[[x_column, y_column]].dropna()

        if len(data) < 2:
            logger.warning(f"Pas assez de données pour scatter plot: {x_column}, {y_column}")
            plt.close(fig)
            return None

        ax.scatter(data[x_column], data[y_column], alpha=0.7, color="steelblue", edgecolors="black", linewidth=0.5)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(title or f"Scatter plot: {x_column} vs {y_column}")
        ax.grid(True, alpha=0.3)

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Scatter plot sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur scatter plot {x_column}/{y_column}: {e}")
        return None


def create_monthly_aggregation_plot(
    df: pd.DataFrame,
    date_column: str,
    output_path: Optional[Union[str, Path]] = None,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> Optional[plt.Figure]:
    """
    Crée un plot des counts par mois (si date_column est une date).

    Returns None si la conversion en datetime échoue.
    """
    if date_column not in df.columns:
        logger.warning(f"Colonne '{date_column}' introuvable pour monthly aggregation")
        return None

    try:
        fig, ax = plt.subplots(figsize=figsize)

        # Copie et conversion datetime
        plot_df = df[[date_column]].copy()
        plot_df = plot_df.dropna(subset=[date_column])

        if len(plot_df) == 0:
            logger.warning(f"Pas de données valides pour {date_column}")
            plt.close(fig)
            return None

        if not pd.api.types.is_datetime64_any_dtype(plot_df[date_column]):
            plot_df[date_column] = pd.to_datetime(plot_df[date_column], errors='coerce')
            plot_df = plot_df.dropna(subset=[date_column])

        if len(plot_df) == 0:
            logger.warning(f"Conversion datetime échouée pour {date_column}")
            plt.close(fig)
            return None

        # Agrégation par mois
        plot_df['year_month'] = plot_df[date_column].dt.to_period('M')
        monthly_counts = plot_df['year_month'].value_counts().sort_index()

        if len(monthly_counts) == 0:
            logger.warning(f"Pas de counts par mois pour {date_column}")
            plt.close(fig)
            return None

        ax.bar(monthly_counts.index.astype(str), monthly_counts.values,
               color="steelblue", alpha=0.7)
        ax.set_xlabel(date_column)
        ax.set_ylabel("Nombre d'occurrences")
        ax.set_title(title or f"Counts par mois - {date_column}")
        ax.grid(True, alpha=0.3, axis="y")
        plt.xticks(rotation=45, ha="right")

        if output_path:
            fig.savefig(output_path, dpi=100, bbox_inches="tight")
            logger.info(f"Monthly aggregation sauvegardé: {output_path}")

        return fig
    except Exception as e:
        logger.warning(f"Erreur monthly aggregation {date_column}: {e}")
        return None


def _apply_viz_suggestion(
    df: pd.DataFrame,
    suggestion: Dict[str, Any],
    figures_dir: Path,
    index: int
) -> Optional[str]:
    """
    Essaie d'appliquer une suggestion de visualisation.

    Returns le chemin du fichier créé ou None.
    """
    viz_type = suggestion.get("type", "").lower()
    columns = suggestion.get("columns", [])
    title = suggestion.get("title", "Visualisation")
    purpose = suggestion.get("purpose", "")

    if viz_type == "histogram" or viz_type == "hist":
        col = columns[0] if columns else None
        if col and col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            path = figures_dir / f"viz_{index}_{col}_hist.png"
            create_histogram(df, col, output_path=path, title=title)
            return str(path)

    elif viz_type == "boxplot":
        col = columns[0] if columns else None
        if col and col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            path = figures_dir / f"viz_{index}_{col}_box.png"
            create_boxplot(df, col, output_path=path, title=title)
            return str(path)

    elif viz_type == "bar" or viz_type == "barchart":
        col = columns[0] if columns else None
        if col and col in df.columns:
            path = figures_dir / f"viz_{index}_{col}_bar.png"
            create_bar_chart(df, col, output_path=path, title=title)
            return str(path)

    elif viz_type == "scatter":
        if len(columns) >= 2:
            x_col, y_col = columns[0], columns[1]
            if (x_col in df.columns and y_col in df.columns and
                pd.api.types.is_numeric_dtype(df[x_col]) and
                pd.api.types.is_numeric_dtype(df[y_col])):
                path = figures_dir / f"viz_{index}_{x_col}_{y_col}_scatter.png"
                create_scatter_plot(df, x_col, y_col, output_path=path, title=title)
                return str(path)

    elif viz_type == "time_series" or viz_type == "timeseries":
        if len(columns) >= 1:
            date_col = columns[0]
            value_col = columns[1] if len(columns) > 1 else None
            if date_col in df.columns:
                if value_col and value_col in df.columns:
                    path = figures_dir / f"viz_{index}_{date_col}_{value_col}_ts.png"
                    create_time_series_plot(df, date_col, value_col, output_path=path, title=title)
                else:
                    path = figures_dir / f"viz_{index}_{date_col}_counts.png"
                    create_monthly_aggregation_plot(df, date_col, output_path=path, title=title)
                return str(path)

    elif viz_type == "heatmap":
        path = figures_dir / f"viz_{index}_corr_heatmap.png"
        # Créer la heatmap à partir des colonnes numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            create_correlation_heatmap(corr_matrix, output_path=path, title=title)
            return str(path)

    logger.warning(f"Visualisation suggestion non applicable: {suggestion}")
    return None


def generate_viz(
    df: pd.DataFrame,
    output_dir: Union[str, Path],
    viz_suggestions: Optional[List[Dict[str, Any]]] = None,
    prefix: str = "analysis"
) -> Dict[str, List[str]]:
    """
    Génère des visualisations dynamiques selon le type des colonnes.

    Si viz_suggestions existe, essaie de les appliquer.

    Args:
        df: Le DataFrame à visualiser
        output_dir: Répertoire de sortie (crée outputs/figures/)
        viz_suggestions: Suggestions de visualisation (optionnel)
        prefix: Préfixe pour les noms de fichiers

    Returns:
        Dict: {type_viz: [chemins]}
    """
    output_dir = Path(output_dir)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    figures = {
        "histograms": [],
        "boxplots": [],
        "barcharts": [],
        "scatterplots": [],
        "timeseries": [],
        "heatmaps": [],
        "custom": []
    }

    # Déterminer les types de colonnes
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64", "datetime64[ns]"]).columns.tolist()

    logger.info(f"Colonnes disponibles: num={len(numeric_cols)}, cat={len(categorical_cols)}, date={len(datetime_cols)}")

    # 1. Histogrammes + Boxplots pour colonnes numériques (top K)
    for col in numeric_cols[:5]:  # Limite à 5 colonnes
        # Histogramme
        hist_path = figures_dir / f"{prefix}_{col}_hist.png"
        if create_histogram(df, col, output_path=hist_path):
            figures["histograms"].append(str(hist_path))

        # Boxplot
        box_path = figures_dir / f"{prefix}_{col}_box.png"
        if create_boxplot(df, col, output_path=box_path):
            figures["boxplots"].append(str(box_path))

    # 2. Bar charts pour colonnes catégorielles (top K, max 5)
    for col in categorical_cols[:5]:
        bar_path = figures_dir / f"{prefix}_{col}_bar.png"
        if create_bar_chart(df, col, output_path=bar_path):
            figures["barcharts"].append(str(bar_path))

    # 3. Monthly aggregation pour colonnes datetime
    for col in datetime_cols:
        monthly_path = figures_dir / f"{prefix}_{col}_monthly.png"
        if create_monthly_aggregation_plot(df, col, output_path=monthly_path):
            figures["timeseries"].append(str(monthly_path))

    # 4. Heatmap de corrélation (si >=2 colonnes numériques)
    if len(numeric_cols) >= 2:
        try:
            corr_matrix = df[numeric_cols].corr()
            if not corr_matrix.empty:
                heatmap_path = figures_dir / f"{prefix}_correlation_heatmap.png"
                if create_correlation_heatmap(corr_matrix, output_path=heatmap_path):
                    figures["heatmaps"].append(str(heatmap_path))
        except Exception as e:
            logger.warning(f"Erreur heatmap: {e}")

    # 5. Appliquer les suggestions personnalisées
    if viz_suggestions:
        for i, suggestion in enumerate(viz_suggestions):
            custom_path = _apply_viz_suggestion(df, suggestion, figures_dir, i)
            if custom_path:
                figures["custom"].append(custom_path)

    logger.info(f"Visualisations générées: {sum(len(v) for v in figures.values())} fichiers")
    return figures


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    print("Module de visualisation de données chargé.")
    print("Utilisez generate_viz(df, output_dir) pour générer des visualisations.")
