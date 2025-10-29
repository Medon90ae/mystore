
from functools import lru_cache
from typing import Annotated, Dict, Any

import firebase_admin.auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from google.cloud import firestore, storage, pubsub_v1, secretmanager
from vertexai.generative_models import GenerativeModel

from .config import settings
from .utils.ai_client import get_vertex_ai_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache
def get_firestore_client() -> firestore.Client:
    return firestore.Client(project=settings.GCP_PROJECT_ID)

@lru_cache
def get_storage_client() -> storage.Client:
    return storage.Client(project=settings.GCP_PROJECT_ID)

@lru_cache
def get_pubsub_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()

@lru_cache
def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, Any]:
    """Dependency to verify Firebase ID token and get user data."""
    try:
        decoded_token = firebase_admin.auth.verify_id_token(token)
        return decoded_token
    except firebase_admin.auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Type alias for dependency injection
CurrentUser = Annotated[Dict[str, Any], Depends(get_current_user)]
FirestoreClient = Annotated[firestore.Client, Depends(get_firestore_client)]
StorageClient = Annotated[storage.Client, Depends(get_storage_client)]
PubSubPublisher = Annotated[pubsub_v1.PublisherClient, Depends(get_pubsub_publisher)]
AIClient = Annotated[GenerativeModel, Depends(get_vertex_ai_client)]
