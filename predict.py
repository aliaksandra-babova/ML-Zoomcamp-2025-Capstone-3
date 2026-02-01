
import pickle

import uvicorn
from fastapi import FastAPI
from typing import Dict, Any

from typing import Literal
from pydantic import BaseModel, Field
from pydantic import ConfigDict

#request

class Sample(BaseModel):
    soil_type: Literal["slightly acidic", "neutral", "alkaline", "acidic"]
    humidity: float = Field(..., ge=0.0, le=40.0)
    phosphorus_level: float = Field(..., ge=0.0, le=40.0)
    soil_moisture: float = Field(..., ge=0.0, le=40.0)
    nitrogen_level: float = Field(..., ge=0.0, le=40.0)

#response

class PredictResponse(BaseModel):
    y_pred: float
    result_status: str
    model_version: str

class Sample(BaseModel):
    model_config = ConfigDict(extra="forbid")

    soil_type: Literal["slightly acidic", "neutral", "alkaline", "acidic"]
    humidity: float = Field(..., ge=0.0, le=100.0)
    phosphorus_level: float = Field(..., ge=0.0, le=100.0)
    soil_moisture: float = Field(..., ge=0.0, le=100.0)
    nitrogen_level: float = Field(..., ge=0.0, le=100.0)    


app = FastAPI(title="plant-stress-prediction")


with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

@app.post("/predict")


def predict(datapoint: Sample) -> PredictResponse:
    dt: Any = pipeline.named_steps['decisiontreeclassifier']
    dv: Any = pipeline.named_steps['dictvectorizer']

    X = dv.transform([datapoint.model_dump()])
    y_pred = int(dt.predict(X)[0])

    health_status_map = {
        0: 'healthy',
        1: 'moderate stress',
        2: 'high stress'
    }

    result_status = health_status_map.get(y_pred, "unknown status")    

    return {
        "prediction_id": y_pred,
        "plant_health_status": result_status,
        "model_version": "decision_tree_v1"
    }

if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=9696)
