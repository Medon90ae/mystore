
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from ..deps import StorageClient, PubSubPublisher, CurrentUser
from ..config import settings
from ..utils.file_handler import upload_to_gcs

router = APIRouter()

@router.post("/upload-xlsx")
async def upload_xlsx(
    user: CurrentUser,
    storage_client: StorageClient,
    publisher: PubSubPublisher,
    file: UploadFile = File(...),
):
    """
    Handles XLSX file upload.
    1. Uploads the file to Google Cloud Storage.
    2. Publishes a message to a Pub/Sub topic with the file's location.
    """
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .xlsx files are accepted.",
        )

    # Generate a unique filename to avoid collisions
    file_path = f"uploads/{user['uid']}/{uuid.uuid4()}-{file.filename}"

    try:
        # Upload file to GCS
        gcs_uri = await upload_to_gcs(storage_client, file, file_path)

        # Publish message to Pub/Sub
        topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.PUBSUB_TOPIC_ID)
        message_data = {
            "gcs_uri": gcs_uri,
            "user_id": user["uid"],
            "filename": file.filename,
        }
        future = publisher.publish(topic_path, data=str(message_data).encode("utf-8"))
        future.result()  # Wait for publish to complete

        return {"message": "File uploaded and processing started.", "gcs_uri": gcs_uri}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
