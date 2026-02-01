# ML-Zoomcamp-2025-Capst    one-3
## Overview
This project focuses on giving value to a farmer by predicting crop stress level based on soil nutrient composition and environmental conditions.

## Problem statement
Early detection of crop stress due to environmental factors.

## Objective: 
The objective of this project is to build a classification model that predicts crop stress level based on available environmental and soil properties data. This model could be incorporated in a Precision Agriculture system that helps farmers implement timely interventions to maintain the crop healthy during growing season.  

## Dataset description
This dataset provides a detailed collection of soil nutrient compositions, environmental conditions, and recommended crops. \
The dataset: [https://catalog.data.gov/dataset/a-regionally-adapted-implementation-of-conservation-agriculture-delivers-rapid-improvement-79c19](https://www.kaggle.com/datasets/aniketkumaraugustya/soil-type-dataset) \ 

# Data Preparation & EDA
## Target Distribution
Target variable: `Plant_Health_Status` \
Type: `str`\
Values: `'High Stress', 'Moderate Stress', 'Healthy'`\
Distribution: `42%, 33% , 25%`

## Missing Values

The dataset has 3400 records, but only 1200 are labeled with Plant_Health_Status, therefore I decided to drop the extra records and further clean up columns that didn't bring any value to the current project objectives. 

## Correlation

Nitrogen_level and Soil_moisture showed the highest negative feature correlation (27% and 77%), which makes agronomical sense, as when moisture and nitrogen levels go down, the stess increases. 

# Model Selection & Training
## Basic Decision Tree Classifier 
Based on feature correlation I selected the following features to train the model:
```
features = ['soil_ph', 'humidity', 'phosphorus_level', 'soil_moisture', 'nitrogen_level']
```
This simple Decision Tree gave `accuracy 0.9958 on validation dataset`.\
\
**Conclusion**: accuracy is high from the start, so we can include soil type instead on soil pH as the feature to simplify required data input.

## Decision Tree Classifier with categorical values 
Decision Tree Classifier: `accuracy 0.9958 on validation dataset` \
\
**Conclusion**: checking feature importance it's clear that **soil moisture** and **nitrogen level** are the most important features, which is expected, so swiping soil pH for simpler soil type doesn't hurt accuracy.

## Decision Tree Classifier parameter tuning

While the initial model reached over 99% accuracy, I performed a grid search on `max_depth` to see if a simpler, more shallow tree (e.g., depth 5) could achieve similar results with less risk of overfitting.\
Final model with `max_depth=5` and `min_samples_leaf=1` stayed at `0.9958 accuracy on validation dataset`.\
\
**Conclusion**: I achieved less complexity for both model input and the model itself keeping high accuracy. 

## Random Forest Classifier
Random Forest Classifier reached `accuracy 0.9958 on validation dataset` out-of-the-box, but parameter tuning didn't give any improvement on validation dataset.\
\
**Conclusion**: I'll proceed to the final training and validation on full training and test data with both models. 

## Final Validation on full dataset
The Decision Tree actually **outperformed** the Random Forest on the test set (0.9958 vs 0.9917). The Random Forest might  be too complex for this specific synthetic data, while a simple Tree captured the "rules" perfectly.\
\
**Conclusion**: **Decision Tree** is a better choice, because it is simpler and more interpretable.

# Future Work:

1. Integrate real-time IoT sensor APIs instead of manual data input.
2. Expand the model to include specific crop types (Corn vs. Wheat) as the current model is a general soil-type baseline.
3. Implement a "History" feature using the Lag features to see health trends over 7 days.
