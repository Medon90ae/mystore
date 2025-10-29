
# Smart Store Backend

This is the backend service for the Smart Store application, built with Python and FastAPI.

## Local Development Setup

### Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- [Google Cloud SDK](https://cloud.google.com/sdk/install)
- A Firebase project and a service account key file.

### 1. Install Dependencies
```bash
poetry install
```

### 2. Set Up Environment Variables
Create a `.env` file in the `smart_store_backend` directory by copying the sample:
```bash
cp .env.sample .env
```
Now, edit the `.env` file with your specific configuration:
- `GCP_PROJECT_ID`: Your Google Cloud project ID.
- `GCS_BUCKET_NAME`: The name of the GCS bucket for uploads.
- `PUBSUB_TOPIC_ID`: The ID of your Pub/Sub topic for XLSX processing.
- `VERTEX_MODEL_SECRET_NAME`: The name of the secret in Secret Manager holding the Vertex model ID.
- `GOOGLE_APPLICATION_CREDENTIALS`: The local path to your Firebase/GCP service account JSON key file.

### 3. Authenticate with GCP
Log in to your GCP account to enable Application Default Credentials (ADC) for the client libraries.
```bash
gcloud auth application-default login
```

### 4. Run the Development Server
```bash
poetry run uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://127.0.0.1:8000`.

## Deployment
Deployment is handled via Google Cloud Build and Cloud Run. Pushing to the main branch of your connected Git repository will trigger the `cloudbuild.yaml` pipeline.

See `DEPLOY_CHECKLIST.md` for the full one-time setup and deployment command sequence.
