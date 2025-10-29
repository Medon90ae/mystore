
#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Replace with your values
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west3"
export SERVICE_NAME="smart-store-backend"
export SERVICE_ACCOUNT_NAME="smart-store-sa"
export ARTIFACT_REPO_NAME="smart-store-repo"
export GCS_BUCKET_NAME="smart-store-uploads-${PROJECT_ID}"
export PUBSUB_TOPIC_ID="xlsx-processing-topic"
export VERTEX_MODEL_SECRET_NAME="vertex-model-id"
export VERTEX_MODEL_ID="gemini-1.5-flash-001" # The model you want to use
export CUSTOM_DOMAIN="api.your-domain.com" # Example custom domain

# --- Setup ---
echo "--- Setting project to ${PROJECT_ID} ---"
gcloud config set project ${PROJECT_ID}

echo "--- Enabling required GCP APIs ---"
gcloud services enable \
  run.googleapis.com \
  iam.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  pubsub.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  bigquery.googleapis.com

echo "--- Creating Service Account: ${SERVICE_ACCOUNT_NAME} ---"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
  --display-name="Smart Store Backend Service Account"

SA_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "--- Granting IAM Roles to Service Account ---"
# Role for Cloud Run
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/run.invoker"
# Role for Storage
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectAdmin"
# Role for BigQuery
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/bigquery.dataEditor"
# Role for Secret Manager
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
# Role for Firestore
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/datastore.user" # Firestore uses datastore roles
# Role for Pub/Sub
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/pubsub.publisher"

echo "--- Creating Artifact Registry repository ---"
gcloud artifacts repositories create ${ARTIFACT_REPO_NAME} \
  --repository-format=docker \
  --location=${REGION} \
  --description="Docker repository for Smart Store"

echo "--- Creating GCS Bucket: ${GCS_BUCKET_NAME} ---"
gcloud storage buckets create gs://${GCS_BUCKET_NAME} --location=${REGION}

echo "--- Creating Pub/Sub Topic: ${PUBSUB_TOPIC_ID} ---"
gcloud pubsub topics create ${PUBSUB_TOPIC_ID}

echo "--- Creating Secret in Secret Manager ---"
gcloud secrets create ${VERTEX_MODEL_SECRET_NAME} --replication-policy="automatic"
echo -n "${VERTEX_MODEL_ID}" | gcloud secrets versions add ${VERTEX_MODEL_SECRET_NAME} --data-file=-

echo "--- Submitting Cloud Build job to build and deploy ---"
gcloud builds submit ./smart_store_backend \
  --config=./smart_store_backend/cloudbuild.yaml \
  --substitutions="_GCS_BUCKET_NAME=${GCS_BUCKET_NAME},_PUBSUB_TOPIC_ID=${PUBSUB_TOPIC_ID},_VERTEX_MODEL_SECRET_NAME=${VERTEX_MODEL_SECRET_NAME}"

echo "--- Mapping custom domain to Cloud Run service ---"
gcloud run domain-mappings create --service ${SERVICE_NAME} --domain ${CUSTOM_DOMAIN} --region ${REGION}

echo "--- Deployment script finished ---"
echo "Please update your DNS records for ${CUSTOM_DOMAIN} with the records shown in the previous step."
echo "It may take some time for the DNS to propagate and the SSL certificate to be provisioned."
