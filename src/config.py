import json
import os


def get_firebase_credentials() -> dict:
    credentials_path: str = "src/firebase-credentials.json"

    if os.path.exists(credentials_path):
        credentials = json.load(open(credentials_path))
    else:
        credentials: dict = json.loads(os.environ.get("SECRET_FIREBASE_CREDENTIALS"))
    return credentials


def get_firebase_api_key() -> str:
    return get_firebase_credentials().get("api_key", "")
