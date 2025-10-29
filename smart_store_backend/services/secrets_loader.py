from google.cloud import secretmanager

def get_secret(secret_name: str, project_id: str) -> str:
    """Retrieve secret value from Google Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
