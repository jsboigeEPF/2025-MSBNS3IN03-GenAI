# Rapport d'Analyse de Données

*Généré le: 2026-02-27 15:04:39*

---

# Aperçu du Dataset

## Informations Générales

| Métrique | Valeur |
|----------|--------|
| Nombre de lignes | 20.00 |
| Nombre de colonnes | 6.00 |
| Taille mémoire | 3.89 KB |
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
| nom | 20.00 | 100.0% |
| date_inscription | 20.00 | 100.0% |

---
# Statistiques Clés

## Statistiques Numériques

| Colonnes | Moyenne | Médiane | Écart-type | Min | Max |
|----------|---------|---------|------------|-----|-----|
| age | 32.75 | 32.50 | 6.34 | 23.00 | 45.00 |
| revenu | 42 350.00 | 42 500.00 | 8 530.29 | 29 000.00 | 61 000.00 |
| score | 83.35 | 83.50 | 6.18 | 72.00 | 93.00 |

## Statistiques Catégorielles

| Colonnes | Valeurs uniques | Mode | Fréquence Mode |
|----------|-----------------|------|----------------|
| nom | 20.00 | Alice | 1.00 |
| ville | 7.00 | Paris | 5.00 |
| date_inscription | 20.00 | 2023-01-15 | 1.00 |

## Corrélations Fortes

| Colonne 1 | Colonne 2 | Corrélation | Force |
|-----------|-----------|-------------|--------|
| age | revenu | 0.99 | strong |
| age | score | 0.95 | strong |
| revenu | score | 0.95 | strong |

---
# Visualisations

## Histogrammes

![analysis_age_hist](figures\analysis_age_hist.png)

![analysis_revenu_hist](figures\analysis_revenu_hist.png)

![analysis_score_hist](figures\analysis_score_hist.png)


## Boxplots

![analysis_age_box](figures\analysis_age_box.png)

![analysis_revenu_box](figures\analysis_revenu_box.png)

![analysis_score_box](figures\analysis_score_box.png)


## Bar Charts

![analysis_date_inscription_bar](figures\analysis_date_inscription_bar.png)

![analysis_nom_bar](figures\analysis_nom_bar.png)

![analysis_ville_bar](figures\analysis_ville_bar.png)


## Scatter Plots

![viz_6_age_revenu_scatter](figures\viz_6_age_revenu_scatter.png)

![viz_7_age_score_scatter](figures\viz_7_age_score_scatter.png)

![viz_8_revenu_score_scatter](figures\viz_8_revenu_score_scatter.png)


## Heatmaps de Corrélation

![analysis_correlation_heatmap](figures\analysis_correlation_heatmap.png)


## Suggestions de Visualisation

| Type | Colonnes | Objectif |
|------|----------|----------|
| histogram | age | Histogramme montrant la distribution des valeurs de age |
| histogram | revenu | Histogramme montrant la distribution des valeurs de revenu |
| histogram | score | Histogramme montrant la distribution des valeurs de score |
| boxplot | age | Boxplot pour détecter les outliers dans age |
| boxplot | revenu | Boxplot pour détecter les outliers dans revenu |
| boxplot | score | Boxplot pour détecter les outliers dans score |
| scatter | age, revenu | Scatter plot avec corrélation de 0.99 |
| scatter | age, score | Scatter plot avec corrélation de 0.95 |
| scatter | revenu, score | Scatter plot avec corrélation de 0.95 |
| bar | ville | Bar chart montrant la répartition des catégories de ville |

---
# Insights et Hypothèses

## Insights Clés

🔵 **1. Dataset de petite taille**

Le dataset contient seulement 20 lignes. Les analyses statistiques peuvent être limitées.

*Recommandation: Considérez collecter plus de données ou utiliser des techniques d'analyse adaptées aux petits échantillons.*

🔵 **2. Colonne nom très unique**

La colonne nom a 20 valeurs uniques sur 20 lignes (100.0%).

🔵 **3. Colonne date_inscription très unique**

La colonne date_inscription a 20 valeurs uniques sur 20 lignes (100.0%).

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
