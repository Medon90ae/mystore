from smart_store_backend.services.secrets_loader import get_secret
from google import genai

PROJECT_ID = "mystore-476317"
API_KEY = get_secret("GOOGLE_CLOUD_API_KEY", PROJECT_ID)

client = genai.Client(vertexai=True, api_key=API_KEY)
