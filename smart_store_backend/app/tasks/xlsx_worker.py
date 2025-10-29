
import base64
import json
import os
from tempfile import NamedTemporaryFile

import pandas as pd
from fastapi import FastAPI, Request, HTTPException, status
from google.cloud import firestore, storage, bigquery

# Configuration
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BQ_DATASET = "shipments_analytics"
BQ_TABLE = "shipments"

# Initialize clients
storage_client = storage.Client()
firestore_client = firestore.Client()
bigquery_client = bigquery.Client()

app = FastAPI()

@app.post("/")
async def process_xlsx(request: Request):
    """
    Receives a push notification from Pub/Sub, processes the corresponding XLSX file.
    """
    envelope = await request.json()
    if not envelope or "message" not in envelope:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Pub/Sub message format",
        )

    pubsub_message = envelope["message"]
    message_data_str = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
    
    # The message data is a string representation of a dict, so we use eval.
    # A more robust solution would be to ensure JSON is published.
    try:
        message_data = eval(message_data_str)
        gcs_uri = message_data["gcs_uri"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid message data format: {e}",
        )

    print(f"Processing file: {gcs_uri}")

    try:
        # 1. Download file from GCS
        bucket_name, blob_name = gcs_uri.replace("gs://", "").split("/", 1)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        with NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
            blob.download_to_filename(temp_file.name)
            temp_filepath = temp_file.name

        # 2. Parse XLSX with pandas
        df = pd.read_excel(temp_filepath)
        os.remove(temp_filepath) # Clean up temp file

        # 3. Write products to Firestore (example)
        # This is a placeholder. Your logic will depend on the XLSX structure.
        batch = firestore_client.batch()
        for _, row in df.iterrows():
            doc_ref = firestore_client.collection("products_from_xlsx").document()
            batch.set(doc_ref, row.to_dict())
        batch.commit()
        print(f"Wrote {len(df)} records to Firestore.")

        # 4. Stream summary to BigQuery (example)
        # This assumes the XLSX has the same schema as the BigQuery table.
        # You would perform transformations here.
        # For this example, we'll just rename columns if needed.
        # df.rename(columns={'Order ID': 'order_id'}, inplace=True)
        table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
        errors = bigquery_client.insert_rows_from_dataframe(table_id, df)
        if not errors:
            print(f"Streamed {len(df)} records to BigQuery.")
        else:
            print(f"Encountered errors while streaming to BigQuery: {errors}")

        return {"status": "success"}

    except Exception as e:
        print(f"Error processing file {gcs_uri}: {e}")
        # Return 500 to have Pub/Sub retry the message
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
