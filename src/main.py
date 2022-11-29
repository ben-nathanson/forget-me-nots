from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from firebase_admin import App, initialize_app

from src.config import CredentialManager
from src.view.routers.account_management_router import account_management_router
from src.view.routers.holiday_router import holiday_router

credential_manager = CredentialManager()
firebase_app: App = initialize_app(credential_manager.get_firebase_cert())
app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
app.include_router(account_management_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, validation_error: RequestValidationError):
    return PlainTextResponse(str(validation_error), status_code=422)
