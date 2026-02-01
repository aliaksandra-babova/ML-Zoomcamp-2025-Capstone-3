ECR_URL=650557269485.dkr.ecr.eu-north-1.amazonaws.com

REPO_URL=${ECR_URL}/mlzoomcamp/plant-stress-prediction-lambda
REMOTE_IMAGE_TAG="${REPO_URL}:v1" 

LOCAL_IMAGE_NAME=plant-stress-prediction-lambda

aws ecr get-login-password \
  --region "eu-north-1" \
| docker login \
  --username AWS \
  --password-stdin ${ECR_URL}

# Build the Docker image
docker build -t ${LOCAL_IMAGE_NAME} .

# Tag the image for ECR
docker tag ${LOCAL_IMAGE_NAME} ${REMOTE_IMAGE_TAG}

# Push the image to ECR
docker push ${REMOTE_IMAGE_TAG}

echo "Image pushed to ECR: ${REMOTE_IMAGE_TAG}"