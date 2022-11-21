from fastapi import FastAPI
from firebase_admin import App, initialize_app
from firebase_admin.credentials import Certificate

from src.config import get_firebase_credentials
from src.view.routers.account_management import account_management_router
from src.view.routers.holiday import holiday_router

firebase_cert: Certificate = Certificate(get_firebase_credentials())
firebase_app: App = initialize_app(firebase_cert)
app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
app.include_router(account_management_router)
