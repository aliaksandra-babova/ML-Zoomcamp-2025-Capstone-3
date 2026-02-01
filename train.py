#!/usr/bin/env python
# coding: utf-8


import pickle

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline


def load_data():

    df = pd.read_csv('/workspaces/ML-Zoomcamp-2025-Capstone-3/soil_with_crop_recommendations.csv')

    df.columns = df.columns.str.lower()

    categorical = list(df.dtypes[df.dtypes == 'str'].index)

    for c in categorical:
        df[c] = df[c].str.lower()

    df = df.drop(columns = ['timestamp', 'crop1', 'crop2', 'crop3', 'label', 'rainfall'])
    
    plant_health_status_values = {
        'moderate stress': 1,
        'high stress': 2,
        'healthy': 0 
    }

    df.plant_health_status = df.plant_health_status.map(plant_health_status_values)

    df.dropna(subset=['plant_health_status'], inplace=True)

    df = df.reset_index(drop=True)

    return df

def train_model(df):
    
    pipeline = make_pipeline(
    DictVectorizer(),
    DecisionTreeClassifier(max_depth=5, min_samples_leaf=1)
    )

    features = ['soil_type', 'humidity', 'phosphorus_level', 'soil_moisture', 'nitrogen_level']

    train_dict = df[features].to_dict(orient='records')
    y_train = df['plant_health_status'].values

    pipeline.fit(train_dict, y_train)
    
    return pipeline



def save_model(filename, model):

    with open(filename, 'wb') as f_out: 
        pickle.dump(model, f_out)

    print(f'Model saved to {filename}')

    return


df = load_data()
pipeline = train_model(df)
save_model('model.bin', pipeline)





