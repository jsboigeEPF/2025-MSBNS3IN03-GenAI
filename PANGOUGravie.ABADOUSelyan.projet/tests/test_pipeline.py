"""
Tests pour le pipeline complet d'analyse de données.

Ce module contient les tests pour vérifier que l'ensemble du pipeline
fonctionne correctement avec des données de test.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil


class TestPipelineIntegration:
    """Tests d'intégration du pipeline complet."""

    def setup_method(self):
        """Crée un répertoire temporaire pour les tests."""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.test_dir) / "outputs"
        self.output_dir.mkdir()

    def teardown_method(self):
        """Nettoie le répertoire temporaire après les tests."""
        shutil.rmtree(self.test_dir)

    @pytest.fixture
    def sample_dataframe(self):
        """Crée un DataFrame d'échantillon pour les tests."""
        np.random.seed(42)
        return pd.DataFrame({
            "nom": ["Alice", "Bob", "Charlie", "David", "Alice", None, "Bob"],
            "âge": [25, 30, 35, 40, 25, None, 30],
            "ville": ["Paris", "Lyon", "Paris", "Marseille", "Paris", "Lyon", "Lyon"],
            "revenu": [50000, 60000, 75000, 80000, 50000, 55000, 62000],
            "score": [85, 90, 78, 92, 85, None, 88]
        })

    def test_pipeline_runs_without_error(self, sample_dataframe):
        """Test que le pipeline s'exécute sans erreur fatale."""
        from src.main import run_analysis_pipeline

        # Sauvegarder le DataFrame en CSV
        input_file = Path(self.test_dir) / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)

        config = {
            "data": {"input_path": str(input_file), "output_dir": str(self.output_dir)},
            "cleaning": {"handle_missing": {"strategy": "fill", "fill_value": "unknown"}},
            "visualization": {"style": "default"},
            "logging": {"level": "ERROR"}  # Réduire le bruit
        }

        # Le test passe si aucune exception n'est levée
        results = run_analysis_pipeline(str(input_file), str(self.output_dir), config, __import__('logging').getLogger())
        assert results is not None
        assert "ingestion" in results

    def test_outputs_generated(self, sample_dataframe):
        """Test que les fichiers de sortie sont générés."""
        from src.main import run_analysis_pipeline

        input_file = Path(self.test_dir) / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)

        config = {
            "data": {"input_path": str(input_file), "output_dir": str(self.output_dir)},
            "cleaning": {"handle_missing": {"strategy": "fill"}},
            "visualization": {"style": "default"},
            "logging": {"level": "ERROR"}
        }

        run_analysis_pipeline(str(input_file), str(self.output_dir), config, __import__('logging').getLogger())

        # Vérifier que les fichiers de sortie existent
        assert (self.output_dir / "execution_results.json").exists()
        assert (self.output_dir / "*.md").exists()
        assert (self.output_dir / "*.html").exists()

    def test_cleaning_handles_missing_values(self, sample_dataframe):
        """Test que le nettoyage gère les valeurs manquantes."""
        from src.clean import handle_missing_values

        df_clean = handle_missing_values(sample_dataframe, strategy="fill", fill_value="unknown")
        assert df_clean.isnull().sum().sum() == 0
        assert len(df_clean) == len(sample_dataframe)

    def test_analysis_returns_results(self, sample_dataframe):
        """Test que l'analyse retourne des résultats."""
        from src.analyze import analyze_data

        results = analyze_data(sample_dataframe)
        assert "shape" in results
        assert "column_stats" in results
        assert results["shape"]["rows"] == len(sample_dataframe)


class TestQAInteraction:
    """Tests pour le système de Questions/Réponses."""

    @pytest.fixture
    def qa_system(self):
        """Crée un système QA pour les tests."""
        np.random.seed(42)
        df = pd.DataFrame({
            "valeur": [10, 20, 30, 40, 50],
            "catégorie": ["A", "B", "A", "C", "B"],
            "date": pd.date_range("2024-01-01", periods=5)
        })
        from src.qa import DataQA
        return DataQA(df)

    def test_answer_count_rows(self, qa_system):
        """Test la réponse à une question de comptage de lignes."""
        answer = qa_system.answer("Combien de lignes?")
        assert "5" in answer or "cinq" in answer.lower()

    def test_answer_column_stats(self, qa_system):
        """Test la réponse à une question de statistiques."""
        answer = qa_system.answer("Quelle est la moyenne?")
        assert "moyenne" in answer.lower() or "30" in answer

    def test_answer_filter(self, qa_system):
        """Test la réponse à une question de filtre."""
        answer = qa_system.answer("Combien de valeur > 20?")
        assert "3" in answer or "trois" in answer.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
