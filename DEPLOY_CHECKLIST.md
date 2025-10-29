
# Smart Store Deployment Checklist

Follow these steps in order to provision your GCP environment and deploy the backend service.

### 1. Set Project Configuration
First, set your project ID and other variables.
```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west3"
export SERVICE_ACCOUNT_NAME="smart-store-sa"

gcloud config set project ${PROJECT_ID}
```

### 2. Enable GCP APIs
```bash
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
```

### 3. Create Service Account
This account will be used by your Cloud Run service.
```bash
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
  --display-name="Smart Store Backend Service Account"
```

### 4. Grant IAM Roles to Service Account
The service account needs permissions to access other GCP services.
```bash
SA_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Allow Cloud Run service to be invoked
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/run.invoker"

# Allow access to GCS buckets
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.objectAdmin"

# Allow access to BigQuery for analytics
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/bigquery.dataEditor"

# Allow access to Secret Manager
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/secretmanager.secretAccessor"

# Allow access to Firestore
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/datastore.user"

# Allow publishing to Pub/Sub
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/pubsub.publisher"
```

### 5. Create Secrets in Secret Manager
Store sensitive information like API keys and model IDs here.
```bash
# Create the secret container
gcloud secrets create vertex-model-id --replication-policy="automatic"

# Add the model ID as the first version of the secret
echo -n "gemini-1.5-flash-001" | gcloud secrets versions add vertex-model-id --data-file=-

# Repeat for other secrets like Twilio keys, etc.
# gcloud secrets create twilio-auth-token --replication-policy="automatic"
# echo -n "your-twilio-token" | gcloud secrets versions add twilio-auth-token --data-file=-
```

### 6. Create Other Infrastructure
- **Artifact Registry**: To store your Docker images.
- **GCS Bucket**: For file uploads.
- **Pub/Sub Topic**: For background tasks.
- **BigQuery Dataset**: For analytics.

```bash
# Create Artifact Registry repo
gcloud artifacts repositories create smart-store-repo \
  --repository-format=docker \
  --location=${REGION}

# Create GCS Bucket
gcloud storage buckets create gs://smart-store-uploads-${PROJECT_ID} --location=${REGION}

# Create Pub/Sub Topic
gcloud pubsub topics create xlsx-processing-topic

# Create BigQuery Dataset
bq --location=${REGION} mk --dataset ${PROJECT_ID}:shipments_analytics
```

### 7. Deploy the Application
Run the `deploy.sh` script or submit the build manually.
```bash
# Make sure you are in the root of your project directory
gcloud builds submit ./smart_store_backend \
  --config=./smart_store_backend/cloudbuild.yaml \
  --substitutions="_GCS_BUCKET_NAME=smart-store-uploads-${PROJECT_ID},_PUBSUB_TOPIC_ID=xlsx-processing-topic,_VERTEX_MODEL_SECRET_NAME=vertex-model-id"
```

### 8. Map Custom Domain (Optional)
After the service is deployed, map your custom domain.
```bash
gcloud run domain-mappings create \
  --service smart-store-backend \
  --domain api.your-domain.com \
  --region ${REGION}
```
Follow the instructions to update your DNS records at your domain provider (e.g., Hostinger).
