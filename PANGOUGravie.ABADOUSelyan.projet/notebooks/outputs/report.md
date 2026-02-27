# Rapport d'Analyse de Données

*Généré le: 2026-02-27 13:58:03*

---

# Aperçu du Dataset

## Informations Générales

| Métrique | Valeur |
|----------|--------|
| Nombre de lignes | 10.00 |
| Nombre de colonnes | 6.00 |
| Taille mémoire | 2.00 KB |
| Données manquantes totales | 0.00 |
| Pourcentage de valeurs manquantes | 0.0% |

## Répartition des Colonnes

- **Numériques**: 3.00 colonnes
- **Catégorielles**: 3.00 colonnes
- **Date/Heure**: 0.00 colonnes

---

# Qualité des Données

## Score de Qualité: ✅ 100.0% (Excellent)

| Métrique | Valeur |
|----------|--------|
| Total de valeurs manquantes | 0.00 |
| Pourcentage de valeurs manquantes | 0.0% |
| Duplicates détectés | 0.00 |

## Colonnes avec des Problèmes de Qualité

### Colonnes avec plus de 10% de valeurs manquantes (0 colonnes)
*Aucune colonne avec plus de 10% de valeurs manquantes.*

### Colonnes à forte cardinalité
*Ces colonnes ont plus de 90% de valeurs uniques.*

| Colonnes | Valeurs uniques | % |
|----------|-----------------|---|
| nom | 10.00 | 100.0% |
| date | 10.00 | 100.0% |

---
# Statistiques Clés

## Statistiques Numériques

| Colonnes | Moyenne | Médiane | Écart-type | Min | Max |
|----------|---------|---------|------------|-----|-----|
| ge | 31.50 | 30.00 | 5.80 | 25.00 | 40.00 |
| revenu | 63 500.00 | 61 000.00 | 13 335.42 | 48 000.00 | 85 000.00 |
| score | 87.90 | 88.00 | 4.68 | 78.00 | 95.00 |

## Statistiques Catégorielles

| Colonnes | Valeurs uniques | Mode | Fréquence Mode |
|----------|-----------------|------|----------------|
| nom | 10.00 | Alice | 1.00 |
| ville | 3.00 | Paris | 5.00 |
| date | 10.00 | 2024-01-15 | 1.00 |

## Corrélations Fortes

| Colonne 1 | Colonne 2 | Corrélation | Force |
|-----------|-----------|-------------|--------|
| ge | revenu | 0.98 | strong |

---
# Visualisations

## Histogrammes

![analysis_ge_hist](figures\analysis_ge_hist.png)

![analysis_revenu_hist](figures\analysis_revenu_hist.png)

![analysis_score_hist](figures\analysis_score_hist.png)


## Boxplots

![analysis_ge_box](figures\analysis_ge_box.png)

![analysis_revenu_box](figures\analysis_revenu_box.png)

![analysis_score_box](figures\analysis_score_box.png)


## Bar Charts

![analysis_date_bar](figures\analysis_date_bar.png)

![analysis_nom_bar](figures\analysis_nom_bar.png)

![analysis_ville_bar](figures\analysis_ville_bar.png)


## Scatter Plots

![viz_6_ge_revenu_scatter](figures\viz_6_ge_revenu_scatter.png)


## Suggestions de Visualisation

| Type | Colonnes | Objectif |
|------|----------|----------|
| histogram | ge | Histogramme montrant la distribution des valeurs de ge |
| histogram | revenu | Histogramme montrant la distribution des valeurs de revenu |
| histogram | score | Histogramme montrant la distribution des valeurs de score |
| boxplot | ge | Boxplot pour détecter les outliers dans ge |
| boxplot | revenu | Boxplot pour détecter les outliers dans revenu |
| boxplot | score | Boxplot pour détecter les outliers dans score |
| scatter | ge, revenu | Scatter plot avec corrélation de 0.98 |
| bar | nom | Bar chart montrant la répartition des catégories de nom |
| bar | ville | Bar chart montrant la répartition des catégories de ville |
| bar | date | Bar chart montrant la répartition des catégories de date |

---
# Insights et Hypothèses

## Insights Clés

🔵 **1. Dataset de petite taille**

Le dataset contient seulement 10 lignes. Les analyses statistiques peuvent être limitées.

*Recommandation: Considérez collecter plus de données ou utiliser des techniques d'analyse adaptées aux petits échantillons.*

🔵 **2. Colonne nom très unique**

La colonne nom a 10 valeurs uniques sur 10 lignes (100.0%).

🔵 **3. Colonne date très unique**

La colonne date a 10 valeurs uniques sur 10 lignes (100.0%).

## Hypothèses à Explorer

**1. Corrélation**

Analyser les corrélations entre variables

*Validation: Calculer corrélations*

---
# Prochaines Étapes

Voici les recommandations pour les prochaines étapes de l'analyse :

3. **Exploration des corrélations** : Plusieurs paires de variables fortement corrélées ont été détectées. Analyser les relations causales.

5. **Générer les visualisations** : 10 visualisations suggérées peuvent être générées pour approfondir l'analyse.

## Plan d'Action Recommandé

| Étape | Action | Priorité |
|-------|--------|----------|
| 1 | Vérification de la qualité des données | Haute |
| 2 | Exploration des corrélations | Moyenne |
| 3 | Génération de visualisations approfondies | Moyenne |
| 4 | Test d'hypothèses | Haute |

---
