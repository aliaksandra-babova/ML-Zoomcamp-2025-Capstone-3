import pickle
import json


with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

def predict(datapoint):
    dt = pipeline.named_steps['decisiontreeclassifier']
    dv = pipeline.named_steps['dictvectorizer']

    # In Lambda, we receive a raw dict, so no model_dump() needed
    X = dv.transform([datapoint])
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

def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    'event' is the JSON payload sent to the function.
    """
    # If using API Gateway, the body might be a stringified JSON
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        # If testing directly in AWS Console
        data = event

    try:
        result = predict(data)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }