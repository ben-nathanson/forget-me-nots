import json
import os

from fastapi import FastAPI
from firebase_admin import App, initialize_app
from firebase_admin.credentials import Certificate

from src.view.routers.account_management import account_management_router
from src.view.routers.holiday import holiday_router

credential_data: dict = os.environ.get(
    "SECRET_FIREBASE_CREDENTIALS", json.load(open("src/firebase-credentials.json"))
)
firebase_cert: Certificate = Certificate(credential_data)
firebase_app: App = initialize_app(firebase_cert)
app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
app.include_router(account_management_router)
