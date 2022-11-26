from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from firebase_admin import App, initialize_app
from starlette.responses import PlainTextResponse

from src.config import CredentialManager
from src.view.routers.account_management import account_management_router
from src.view.routers.holiday import holiday_router

credential_manager = CredentialManager()
firebase_app: App = initialize_app(credential_manager.get_firebase_cert())
app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
app.include_router(account_management_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, validation_error: RequestValidationError):
    return PlainTextResponse(str(validation_error), status_code=422)
