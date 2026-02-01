import boto3
import json

lambda_client = boto3.client('lambda')

datapoint = {
    "soil_type": "slightly acidic",
    "humidity": 40,
    "phosphorus_level": 12.7,
    "soil_moisture": 14.4,
    "nitrogen_level": 45.5
}

response = lambda_client.invoke(
    FunctionName='plant-stress-prediction-docker',
    InvocationType='RequestResponse',
    Payload=json.dumps(datapoint)
)

result = json.loads(response['Payload'].read())
print(json.dumps(result, indent=2))