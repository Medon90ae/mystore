
from functools import lru_cache
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import secretmanager

from ..config import settings

@lru_cache
def get_model_id_from_secret_manager() -> str:
    """Fetches the Vertex AI model ID from Google Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{settings.GCP_PROJECT_ID}/secrets/{settings.VERTEX_MODEL_SECRET_NAME}/versions/{settings.SECRET_VERSION}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Could not fetch secret from Secret Manager: {e}. Falling back to default.")
        # Fallback for local development if secret isn't set
        return "gemini-1.5-flash-001"

@lru_cache
def get_vertex_ai_client() -> GenerativeModel:
    """
    Initializes the Vertex AI client and returns a GenerativeModel instance.
    Uses Application Default Credentials.
    """
    vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    
    model_id = get_model_id_from_secret_manager()
    
    model = GenerativeModel(model_id)
    return model
