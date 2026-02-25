
# 🤖 AI Code Reviewer - Assistant de Revue de Code Intelligent

Ce projet a été réalisé par **Robin et Nathan** dans le cadre de nos études (E3). Il s'agit d'une application web complète conçue pour automatiser et enrichir le processus de **Code Review** (revue de code) sur GitHub grâce à l'Intelligence Artificielle.

Plus qu'un simple générateur de rapports, cet outil agit comme un véritable mentor technique capable de s'adapter au niveau du développeur et d'échanger avec lui de manière interactive.

---

## ✨ Fonctionnalités Principales

* **🔍 Extraction Automatique :** Connexion transparente à l'API publique de GitHub pour récupérer les modifications exactes (le "Diff") d'une Pull Request.
* **🎓 Pédagogie Adaptative (Prompt Engineering) :** * *Mode Junior :* L'IA agit comme un mentor bienveillant. Elle vulgarise, explique le "pourquoi" des erreurs et commente abondamment le code corrigé.
  * *Mode Senior :* L'IA va droit au but avec des retours purement techniques (architecture, failles critiques, optimisation).
* **💬 Chatbot Interactif Intégré :** Une fois le rapport généré, l'utilisateur peut discuter directement avec l'IA pour lui demander des précisions sur une faille, lui faire réécrire une fonction, ou débattre d'un choix architectural (l'IA garde en mémoire tout le contexte du code).
* **🔐 Espace Personnel Sécurisé :** Système d'authentification complet avec hachage cryptographique des mots de passe (`Werkzeug`).
* **📚 Historique Persistant :** Sauvegarde automatique des revues en base de données (MySQL) pour y revenir à tout moment.

---

## 🛠️ Stack Technique

* **Backend :** Python 3, Flask, SQLAlchemy (ORM).
* **Frontend :** HTML5, CSS3 (Vanilla, design moderne), JavaScript (Fetch API, DOM manipulation).
* **Base de données :** MySQL (via PyMySQL).
* **Intelligence Artificielle :** API OpenRouter (modèle `anthropic/claude-3.5-sonnet` optimisé pour le code).
* **Autres :** `requests` (Appels API GitHub), `marked.js` (Rendu Markdown en HTML).

---

## 📁 Architecture du Projet (Modèle-Vue-Contrôleur)

```text
projet-revieweur-ia/
├── app.py                # Point d'entrée, Serveur web Flask & Routes API
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Variables d'environnement secrètes (Clé API) - NON INCLUS
├── src/                  # Logique métier ("Cerveau" de l'application)
│   ├── config.py         # Chargement sécurisé de la configuration
│   ├── git_parser.py     # Communication avec l'API REST de GitHub
│   └── ai_reviewer.py    # Logique IA, Prompts, et gestion de la mémoire du Chat
└── templates/            # Vues (Interface Utilisateur)
    ├── index.html        # Page principale : Analyse et Chat interactif
    ├── login.html        # Page de connexion
    ├── register.html     # Page d'inscription
    └── historique.html   # Tableau de bord listant les anciennes analyses
```
