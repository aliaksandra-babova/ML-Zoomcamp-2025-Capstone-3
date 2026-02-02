# ML-Zoomcamp-2025-Capstone-3
## Overview
This project focuses on giving value to a farmer by predicting crop stress level based on soil nutrient composition and environmental conditions.

## Problem statement
Early detection of crop stress due to environmental factors.

## Objective: 
The objective of this project is to build a classification model that predicts crop stress level based on available environmental and soil properties data. This model could be incorporated in a Precision Agriculture system that helps farmers implement timely interventions to maintain the crop healthy during growing season.  

## Dataset description
This dataset provides a detailed collection of soil nutrient compositions, environmental conditions, and recommended crops. \
The dataset: https://www.kaggle.com/datasets/aniketkumaraugustya/soil-type-dataset 

# Data Preparation & EDA
## Target Distribution
Target variable: `Plant_Health_Status` \
Type: `str`\
Values: `'High Stress', 'Moderate Stress', 'Healthy'`\
Distribution: `42%, 33% , 25%`

## Missing Values

The dataset has 3400 records, but only 1200 are labeled with `Plant_Health_Status`, therefore I decided to drop the extra records and further clean up columns that didn't bring any value to the current project objectives. 

## Correlation

`Nitrogen_level` and `Soil_moisture` showed the highest negative feature correlation (**27%** and **77%**), which makes agronomical sense, as when moisture and nitrogen levels go down, the stess increases. 

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
**Conclusion**: **Decision Tree** is a better choice, because it is simpler and more interpretable.\
\
**NOTE**: During hyperparameter tuning, multiple configurations (depths 4-6) yielded identical accuracy. While the final model uses `max_depth=5`, a depth of 4 with a higher `min_samples_leaf` (e.g., 15) would likely provide even better generalization and interpretability, as it prevents the model from creating branches for very specific, potentially noisy data points.

# Testing the predictions
## Running locally
1. Clone the repo:
```
git clone https://github.com/aliaksandra-babova/ML-Zoomcamp-2025-Capstone-3
```
2. Install uv:
```
pip install uv
```
3. Switch directory:
```
cd ML-Zoomcamp-2025-Capstone-3
```
4. Install the project's dependencies:
```
uv sync
```
5. Run the app with uvicorn inside the virtual environment: 
```
uv run uvicorn predict:app --host 0.0.0.0 --port 9696 --reload
```
6. Send a request via the api docs (http://localhost:9696/docs) or with this curl:
```
curl -X 'POST' 'http://localhost:9696/predict' -H 'Content-Type: application/json' -d '{"soil_type": "slightly acidic", "humidity": 40, "phosphorus_level": 12, "soil_moisture": 14, "nitrogen_level": 45}'
```
7. You can also run the service.py script:
```
uv run python request.py
```
## Running Docker
1. Switch directory:
```
cd ML-Zoomcamp-2025-Capstone-3
```
2. Build the docker image:
```
docker build -t plant-stress-prediction .
```
3. Run it:
```
docker run -it --rm -p 9696:9696 plant-stress-prediction
```
4. Send a request via the api docs (http://localhost:9696/docs) or with this curl: 
```
curl -X 'POST' 'http://localhost:9696/predict' -H 'Content-Type: application/json' -d '{"soil_type": "slightly acidic", "humidity": 40, "phosphorus_level": 12, "soil_moisture": 14, "nitrogen_level": 45}'
```
5. You can also run the service.py script:
```
python request.py
```
# Serverless deployment

The final model is containerized using Docker and deployed as a serverless function on AWS Lambda.

## Local Deployment (Docker)

1. Switch directory:
```
cd serverless
```
2. Build the docker image:
```
docker build -t plant-stress-prediction .
```
3. Run it (it can take some time):
```
docker run -it --rm -p 8080:8080 plant-stress-prediction
```
4. Test the local endpoint: In a new terminal, run the following curl command:
```
curl -X 'POST' "http://localhost:8080/2015-03-31/functions/function/invocations" \
-d '{"soil_type": "slightly acidic", "humidity": 40, "phosphorus_level": 12.7, "soil_moisture": 14.4, "nitrogen_level": 45.5}'
```
## Remote Deployment (AWS Lambda)
The model is hosted on AWS. You can test the live endpoint using the following Python script:
1. Switch directory:
```
cd serverless
```
2. Run the invoke.py script:
```
python invoke.py
```
**NOTES**: 
1. The script requires boto3, if missing, install with:
```
pip install boto3
```
2. To test the remote Lambda function, please provide your own AWS credentials. In the terminal, run the following before executing the test script:
```
export AWS_ACCESS_KEY_ID="aws_access_key"
export AWS_SECRET_ACCESS_KEY="aws_secret_key"
export AWS_DEFAULT_REGION="eu-north-1"
```

# Reproducibility & Environment Management
To ensure the results are 100% reproducible across different environments, this project utilizes modern dependency and environment management tools:

* **Environment Isolation**: Developed using `uv` to ensure strict version pinning of the libraries.

* **Cross-Platform Consistency**: The project was verified in a clean **GitHub Codespaces** environment to simulate a "first-time user" experience.

* **Cloud-Ready Infrastructure**: The deployment is fully containerized, allowing the model to transition from a local FastAPI server to an AWS Lambda function without modification to the core logic.

# Technical Challenges & Lessons Learned
During development, several key challenges were addressed:

* **Model Selection**: Initial **Logistic Regression** yielded a baseline accuracy of 76%. Transitioning to a **Decision Tree** allowed the model to capture non-linear sensor relationships, increasing accuracy to **99.5%**.

* **Feature Optimization**: By analyzing feature importance, it was determined that `soil_moisture` and `nitrogen_level` were the primary drivers. This allowed the substitution of `soil_pH` with the more accessible `soil_type` feature without compromising performance.

* **Production Debugging**: Encountered and resolved a nested JSON structure issue during `Lambda` deployment where the `DictVectorizer` required a flat dictionary input.
* **Configuration Portability**: Resolved `NoRegionError` and credential handling in `boto3` by transitioning from local file-based configs to environment variables (`AWS_DEFAULT_REGION`), ensuring the `invoke.py` script works for any reviewer with valid credentials.

# Future Work:

1. Integrate real-time IoT sensor APIs instead of manual data input.
2. Expand the model to include specific crop types (Corn vs. Wheat) as the current model is a general soil-type baseline.
3. Implement a "History" feature using the Lag features to see health trends over 7 days.
