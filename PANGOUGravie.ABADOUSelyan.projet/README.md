# Data Analyst Agent

Un agent d'analyse de données automatisé en Python. Analysez, visualisez et posez des questions sur vos données en quelques secondes.

## 📋 Fonctionnalités

- **Ingestion de données** : Chargement CSV/Excel avec détection automatique (séparateur, encoding)
- **Nettoyage** : Gestion des valeurs manquantes, outliers, normalisation
- **Analyse** : Statistiques descriptives, corrélation, qualité des données
- **Visualisation** : Histogrammes, boxplots, scatter plots, time series
- **Rapports** : Génération de rapports Markdown/HTML
- **Questions/Réponses** : Interrogez vos données en langage naturel
  - **Mode LLM** : OpenAI Responses API avec tool calling (gpt-4o par défaut)
  - **Fallback rule-based** : En absence de clé API, réponse par analyse de patterns

## 🛠️ Installation

```bash
# Cloner le dépôt
git clone <url-du-depot>
cd PANGOUGravie.ABADOUSelyan.projet

# Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer OpenAI API (optionnel)
cp .env.example .env
# Éditer .env et ajouter votre clé:
# OPENAI_API_KEY=sk-votre_clé_ici
```

## 📁 Structure du projet

```
PANGOUGravie.ABADOUSelyan.projet/
├── src/              # Code source
│   ├── __init__.py
│   ├── ingest.py     # Chargement des données
│   ├── clean.py      # Nettoyage
│   ├── analyze.py    # Analyse statistique
│   ├── viz.py        # Visualisation
│   ├── report.py     # Génération de rapports
│   ├── llm.py        # Wrapper OpenAI (LLM)
│   ├── qa.py         # Questions/Réponses (LLM + rule-based)
│   ├── main.py       # Point d'entrée
│   └── config_env.py # Configuration .env
├── notebooks/        # Notebooks Jupyter
│   └── Data_Analyst_Agent.ipynb
├── tests/            # Tests unitaires
│   ├── test_pipeline.py
│   └── test_modules.py
├── outputs/          # Résultats générés
│   ├── figures/      # Visualisations PNG
│   ├── report.md     # Rapport Markdown
│   └── summary.json  # Résumé complet
├── logs/             # Logs d'exécution
├── config.yaml       # Configuration
└── requirements.txt  # Dépendances
```

## 🚀 Utilisation

### Ligne de commande

**Analyser un fichier CSV :**
```bash
python -m src.main data/mon_fichier.csv
```

**Avec configuration personnalisée :**
```bash
python -m src.main data/mon_fichier.csv -c config.yaml -o outputs/
```

**Mode interactif (ask - posez des questions sur vos données) :**
```bash
python -m src.main --interactive
```

### Programme Python

```python
from src.ingest import load_data
from src.clean import clean_data
from src.analyze import analyze_data
from src.viz import generate_viz
from src.report import generate_report
from src.qa import DataQA

# Charger les données
df = load_data("data/input.csv")

# Nettoyer
df_clean = clean_data(df)

# Analyser
analysis_summary, insights, viz_suggestions = analyze_data(df_clean)

# Visualiser
figures = generate_viz(df_clean, "outputs/")

# Générer un rapport
generate_report(analysis_summary, "outputs/")

# Questions/Réponses (LLM ou rule-based)
qa = DataQA(df_clean)
print(qa.answer("Combien de lignes?"))
```

### Configuration LLM

Le mode LLM est contrôlé par `config.yaml` :

```yaml
llm:
  enabled: true          # Activer/désactiver l'LLM (défaut: true)
  model: "gpt-4o"        # Modèle à utiliser
  temperature: 0.2       # Créativité (0 = déterministe, 1 = créatif)
  max_output_tokens: 800

  security:
    prevent_code_execution: true  # Bloquer exec/eval
    max_query_cost: 0.10          # USD max par requête
    max_queries_per_minute: 10
```

**Fallback** : En absence de `OPENAI_API_KEY` ou si `llm.enabled: false`, le mode rule-based est utilisé automatiquement.

**Pour désactiver l'LLM :**
- Soit supprimer la clé API de `.env`
- Soit mettre `enabled: false` dans `config.yaml`

## 📓 Jupyter Notebook

Un notebook interactif est disponible pour une utilisation plus visuelle :

### Lancer le notebook

```bash
# Via Jupyter Notebook
jupyter notebook notebooks/Data_Analyst_Agent.ipynb

# Via Jupyter Lab (interface plus avancée)
jupyter lab notebooks/Data_Analyst_Agent.ipynb

# Ou lancer tout le serveur
jupyter notebook
```

### Configuration requise

Avant de lancer le notebook, assurez-vous que :

1. **Vous avez installé les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

2. **Vous avez créé le fichier `.env` avec votre clé API :**
   ```bash
   cp .env.example .env
   # Éditer .env et ajouter votre clé:
   # OPENAI_API_KEY=sk-votre_clé_ici
   ```

3. **Vous avez installé les dépendances Jupyter (déjà incluses dans requirements.txt) :**
   ```bash
   pip install jupyter ipykernel
   ```

### Utilisation du notebook

Le notebook `notebooks/Data_Analyst_Agent.ipynb` :

1. Charge la configuration (`config.yaml`)
2. Charge vos clés API depuis `.env`
3. Vous demande le chemin du fichier CSV (`DATA_PATH`)
4. Exécute le pipeline complet (ingest → clean → analyze → viz → report)
5. Affiche :
   - Un aperçu du DataFrame (head)
   - Un résumé de la qualité des données
   - Les insights générés (LLM ou rule-based)
   - Les visualisations générées (affichage inline)
   - Un lien vers le rapport généré (`outputs/report.md`)

### Avantages du notebook

- Interface interactive et visuelle
- Possibilité d'exécuter les cellules une par une
- Visualisation immédiate des résultats
- Documentation intégrée dans le notebook
- Idéal pour l'exploration de données et le débogage

## ⚙️ Configuration

Modifiez `config.yaml` pour personnaliser le comportement :

```yaml
data:
  input_path: "data/input.csv"
  output_dir: "outputs"
  encoding: "utf-8"
  separator: ","

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Lancer un fichier spécifique
pytest tests/test_pipeline.py -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html
```

## 📊 Contraintes du projet

- Python 3.11+
- pandas, numpy, matplotlib (pas seaborn)
- Robuste à tout type de CSV (pas de supposition de colonnes)
- Logs clairs pour le débogage

## 🔑 Sécurité

- La clé API OpenAI **n'est jamais stockée en dur**
- Elle est lue depuis la variable d'environnement `OPENAI_API_KEY`
- Le mode rule-based s'active automatiquement si la clé est absente
- Le code exécuté par l'LLM est validé (pas de `exec()`/`eval()` arbitraire)

## 📝 License

Propriétaire - Gravie ABADOUSelyan
