
import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, products, upload, chat
from .config import settings

# Initialize Firebase Admin SDK
# On Cloud Run, ADC will be used automatically if no credential is provided.
# For local dev, set GOOGLE_APPLICATION_CREDENTIALS env var.
try:
    firebase_admin.initialize_app(options={'projectId': settings.GCP_PROJECT_ID})
    print("Firebase Admin SDK initialized successfully.")
except ValueError:
    print("Firebase Admin SDK already initialized.")


app = FastAPI(
    title="Smart Store Backend",
    description="API for the Smart Store application, powering products, uploads, and AI chat.",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Smart Store Backend API!"}
