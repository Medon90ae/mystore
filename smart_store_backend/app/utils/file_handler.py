
from fastapi import UploadFile
from google.cloud import storage
from ..config import settings

async def upload_to_gcs(client: storage.Client, file: UploadFile, destination_blob_name: str) -> str:
    """Uploads a file to the GCS bucket."""
    bucket = client.bucket(settings.GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    # Read file content into memory
    contents = await file.read()
    
    # Upload from memory
    blob.upload_from_string(
        contents,
        content_type=file.content_type
    )

    return f"gs://{settings.GCS_BUCKET_NAME}/{destination_blob_name}"
