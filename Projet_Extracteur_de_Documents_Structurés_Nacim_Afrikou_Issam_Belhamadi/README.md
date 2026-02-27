# 📄 Extracteur de Documents Structurés - NAF_ISB

Projet de traitement automatisé de documents (factures, commandes) avec extraction structurée via IA générative (OpenAI GPT-4o-mini).

**Auteurs :** Nacim Afrikou, Issam Belhamadi
**Module :** MSBNS3IN03 - IA Générative
**Année :** 2026

---

## 🚀 Fonctionnalités

- **Extraction automatique** depuis PDF, Word, Excel, CSV et fichiers texte
- **Détection intelligent** du type de document (facture / commande)
- **Structured Outputs** OpenAI pour garantir des JSON valides
- **Interface web** Streamlit pour un traitement interactif
- **CLI** pour le traitement en ligne de commande

---

## 🛠️ Architecture

```
src/
├── __init__.py
├── main.py          # Point d'entrée CLI
├── models.py        # Modèles Pydantic (Order, Invoice)
├── llm_client.py    # Client OpenAI avec Structured Outputs
└── extractors.py    # Pipeline d'extraction de texte
interface/
└── app.py           # Interface Streamlit
```

---

## 📦 Installation

```bash
# Cloner le projet
git clone <repo-url>
cd Projet_Extracteur_de_Documents_Structurés_Nacim_Afrikou_Issam_Belhamadi/Projet_Extracteur_de_Documents_Structurés_Nacim_Afrikou_Issam_Belhamadi

# Créer l'environnement virtuel
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API OpenAI
cp .env.example .env
# Éditer .env avec votre OPENAI_API_KEY
```

---

## 🚀 Utilisation

### Mode CLI

```bash
# Traiter tous les fichiers de data/input
python -m src.main

# Traiter un fichier spécifique
python -m src.main data/input/facture.pdf

# Traiter un dossier
python -m src.main -f data/input
```

### Mode Interface Web

```bash
streamlit run interface/app.py
```

### Batch (Windows)

Double-cliquer sur `run.bat` ou `run_main.bat`.

---

## 📊 Formats Supportés

| Format | Extension |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx` |
| Texte | `.txt`, `.text` |
| Excel | `.xlsx`, `.xls` |
| CSV | `.csv` |

---

## 📋 Modèles de Données

### Order (Commande)
```json
{
  "document_type": "order",
  "order_id": "10999",
  "order_date": "2018-04-03",
  "customer_name": "Ottilies Käseladen",
  "products": [...],
  "total_price": 1261.0
}
```

### Invoice (Facture)
```json
{
  "document_type": "invoice",
  "invoice_number": "FAC-2024-001",
  "seller": { "name": "...", "address": "..." },
  "items": [...],
  "subtotal": 1500.0,
  "total": 1800.0
}
```

---

## 🔧 Dépendances

- `pdfplumber` - Extraction texte depuis PDF
- `pydantic` - Modèles de données
- `openai` - Client API OpenAI
- `streamlit` - Interface web
- `python-docx` - Fichiers Word
- `pandas` - Fichiers Excel/CSV

---

## 📄 License

MIT License - Copyright (c) 2026 jsboigeEPF
