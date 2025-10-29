
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GCP_PROJECT_ID: str
    GCP_REGION: str = "europe-west3"
    GCS_BUCKET_NAME: str
    PUBSUB_TOPIC_ID: str
    VERTEX_MODEL_SECRET_NAME: str
    SECRET_VERSION: str = "latest"

    # For local development, load from a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()
