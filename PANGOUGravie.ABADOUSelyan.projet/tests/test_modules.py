"""
Tests unitaires pour les modules individuels.

Ce module contient les tests unitaires pour chaque module du package
src: ingest, clean, analyze, viz, report, qa.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Mode sans affichage


class TestIngestModule:
    """Tests pour le module ingest."""

    def test_load_csv_basic(self, tmp_path):
        """Test le chargement d'un CSV basique."""
        from src.ingest import load_csv

        csv_file = tmp_path / "test.csv"
        csv_file.write_text("col1,col2\n1,2\n3,4\n")

        df = load_csv(csv_file)
        assert len(df) == 2
        assert list(df.columns) == ["col1", "col2"]

    def test_load_csv_missing_file(self):
        """Test le comportement avec un fichier manquant."""
        from src.ingest import load_csv
        from FileNotFoundError:

        with pytest.raises(FileNotFoundError):
            load_csv("/path/non/existant/file.csv")

    def test_load_csv_empty_file(self, tmp_path):
        """Test le comportement avec un fichier vide."""
        from src.ingest import load_csv

        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        with pytest.raises(ValueError):
            load_csv(csv_file)


class TestCleanModule:
    """Tests pour le module clean."""

    def test_handle_missing_drop(self):
        """Test la suppression des lignes avec valeurs manquantes."""
        from src.clean import handle_missing_values

        df = pd.DataFrame({"a": [1, 2, None], "b": [4, None, 6]})
        df_clean = handle_missing_values(df, strategy="drop")

        assert len(df_clean) == 1
        assert not df_clean.isnull().any().any()

    def test_handle_missing_fill(self):
        """Test le remplissage des valeurs manquantes."""
        from src.clean import handle_missing_values

        df = pd.DataFrame({"a": [1, 2, None], "b": [4, None, 6]})
        df_clean = handle_missing_values(df, strategy="fill", fill_value=0)

        assert len(df_clean) == 3
        assert df_clean.isnull().sum().sum() == 0

    def test_normalize_text(self):
        """Test la normalisation des textes."""
        from src.clean import normalize_text

        df = pd.DataFrame({
            "text": ["  Hello World  ", "  TEST  DATA  ", None]
        })
        df_norm = normalize_text(df)

        assert df_norm.loc[0, "text"] == "hello world"
        assert df_norm.loc[1, "text"] == "test data"

    def test_convert_dtypes(self):
        """Test la conversion automatique des types."""
        from src.clean import convert_dtypes

        df = pd.DataFrame({
            "str_num": ["1", "2", "3"],
            "bool_str": ["true", "false", "true"]
        })
        df_conv = convert_dtypes(df)

        assert pd.api.types.is_numeric_dtype(df_conv["str_num"])
        assert pd.api.types.is_bool_dtype(df_conv["bool_str"])


class TestAnalyzeModule:
    """Tests pour le module analyze."""

    def test_describe_data(self):
        """Test la description statistique des données."""
        from src.analyze import describe_data

        df = pd.DataFrame({
            "a": [1, 2, 3, 4, 5],
            "b": ["x", "y", "x", "z", "y"]
        })

        desc = describe_data(df)
        assert "a" in desc.index
        assert desc.loc["count", "a"] == 5

    def test_get_column_stats_numeric(self):
        """Test les stats pour une colonne numérique."""
        from src.analyze import get_column_stats

        df = pd.DataFrame({"valeur": [10, 20, 30, 40, 50]})
        stats = get_column_stats(df, "valeur")

        assert stats["mean"] == 30.0
        assert stats["min"] == 10.0
        assert stats["max"] == 50.0

    def test_correlation_analysis(self):
        """Test l'analyse de corrélation."""
        from src.analyze import correlation_analysis

        df = pd.DataFrame({
            "a": [1, 2, 3, 4, 5],
            "b": [2, 4, 6, 8, 10],
            "c": ["x", "y", "z", "w", "v"]
        })

        corr = correlation_analysis(df)
        assert len(corr) == 2  # Seules les colonnes numériques
        assert abs(corr.loc["a", "b"] - 1.0) < 0.01  # Corrélation parfaite


class TestVizModule:
    """Tests pour le module viz."""

    def test_create_histogram(self, tmp_path):
        """Test la création d'un histogramme."""
        from src.viz import create_histogram

        df = pd.DataFrame({"valeur": np.random.normal(0, 1, 100)})
        fig = create_histogram(df, "valeur", output_path=tmp_path / "hist.png")

        assert fig is not None
        assert (tmp_path / "hist.png").exists()

    def test_create_scatter_plot(self, tmp_path):
        """Test la création d'un scatter plot."""
        from src.viz import create_scatter_plot

        df = pd.DataFrame({
            "x": np.random.normal(0, 1, 50),
            "y": np.random.normal(0, 1, 50)
        })
        fig = create_scatter_plot(df, "x", "y", output_path=tmp_path / "scatter.png")

        assert fig is not None
        assert (tmp_path / "scatter.png").exists()


class TestReportModule:
    """Tests pour le module report."""

    def test_generate_markdown_report(self, tmp_path):
        """Test la génération d'un rapport Markdown."""
        from src.report import generate_markdown_report

        results = {
            "shape": {"rows": 100, "columns": 10},
            "memory_usage": 1024,
            "quality_issues": {
                "missing_values": [],
                "high_cardinality": []
            },
            "column_stats": {
                "col1": {
                    "dtype": "int64",
                    "count": 100,
                    "missing_count": 0,
                    "missing_percentage": 0.0,
                    "unique_count": 50
                }
            }
        }

        md_content = generate_markdown_report(results, output_path=tmp_path / "report.md")

        assert "# " in md_content
        assert (tmp_path / "report.md").exists()


class TestQAIntegration:
    """Tests d'intégration pour le système QA."""

    def test_dataqa_initialization(self):
        """Test l'initialisation du système QA."""
        from src.qa import DataQA

        df = pd.DataFrame({
            "valeur": [1, 2, 3, 4, 5],
            "cat": ["a", "b", "a", "c", "b"]
        })
        qa = DataQA(df)

        assert len(qa.column_types) == 2
        assert qa.df.shape == (5, 2)

    def test_answer_summary(self):
        """Test la réponse de résumé."""
        from src.qa import DataQA

        df = pd.DataFrame({
            "a": [1, 2, 3, 4, 5],
            "b": ["x", "y", "x", "z", "y"]
        })
        qa = DataQA(df)

        answer = qa.answer("Résumé")
        assert "lignes" in answer.lower() or "colonnes" in answer.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
