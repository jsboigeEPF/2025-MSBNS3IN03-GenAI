
# 🤖 E3 - Revieweur de Code IA (Version Web Complète)

Ce projet a été réalisé dans le cadre de mes études. Il s'agit d'une application web complète développée en Python (Flask) et HTML/CSS/JS "Vanilla" qui automatise la revue de code (Code Review) en analysant les Pull Requests GitHub à l'aide de l'Intelligence Artificielle (Google Gemini).

## 🎯 Objectifs et Fonctionnalités

1. **Parser les diffs et Pull Requests :** Récupération automatique du code modifié via l'API officielle de GitHub.
2. **Détecter les bugs et failles :** L'IA identifie les problèmes de logique, de sécurité et de respect des conventions.
3. **Prompt Engineering Dynamique :** Un sélecteur permet d'adapter le ton de l'IA selon la cible de la revue (Pédagogique pour les "Juniors" ou Direct/Technique pour les "Seniors").
4. **Authentification Sécurisée :** Système de création de compte et de connexion. Les mots de passe sont hachés cryptographiquement via `Werkzeug` (normes de sécurité standards).
5. **Base de Données et Historique :** Sauvegarde automatique des revues générées dans une base de données relationnelle MySQL (gérée via `SQLAlchemy`), accessible depuis un espace personnel.

## 📁 Architecture du projet

Le projet suit une architecture Client-Serveur avec une base de données (Modèle-Vue-Contrôleur) :

```text
projet-revieweur-ia/
├── app.py                # Serveur web Flask (Routage, Authentification, BDD)
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Variables d'environnement secrètes (Clé API)
├── src/                  # Logique métier ("Cerveau" de l'application)
│   ├── config.py         # Chargement sécurisé de la configuration
│   ├── git_parser.py     # Communication avec l'API REST de GitHub
│   └── ai_reviewer.py    # Communication avec l'API Google GenAI et Prompting
└── templates/            # Vues (Frontend : HTML, CSS "Vanilla", JS)
    ├── index.html        # Page principale d'analyse avec sélecteur de niveau
    ├── login.html        # Page de connexion
    ├── register.html     # Page d'inscription
    └── historique.html   # Tableau de bord listant les anciennes analyses
```
