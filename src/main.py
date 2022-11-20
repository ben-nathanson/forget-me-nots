from os import environ

from fastapi import FastAPI
from firebase_admin import App, initialize_app

from src.view.routers.account_management import account_management_router
from src.view.routers.holiday import holiday_router

FIREBASE_CREDENTIALS_PATH = "src/firebase-credentials.json"
environ["GOOGLE_APPLICATION_CREDENTIALS"] = FIREBASE_CREDENTIALS_PATH


firebase_app: App = initialize_app()
app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
app.include_router(account_management_router)
