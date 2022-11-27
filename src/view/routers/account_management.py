from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import src.view.models as view_models
from src.logic.services.account_management import (
    AccountManagementService,
    AuthenticationError,
    SessionToken,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

account_management_router = APIRouter(prefix="/users", tags=["users"])

account_management_service = AccountManagementService()


@account_management_router.post("/create")
def create_user(payload: view_models.CreateUserPayload):
    try:
        account_management_service.create_user(payload.email, payload.password)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))


@account_management_router.post(
    "/login",
    response_model=view_models.LoginResponse,
    responses={403: {"description": "Authentication error."}},
)
def login(payload: view_models.LoginPayload):
    try:
        session_token: SessionToken = account_management_service.login(
            payload.email, payload.password
        )
    except AuthenticationError as error:
        raise HTTPException(status_code=403, detail=str(error))
    return view_models.LoginResponse(
        email=session_token.email,
        expires_in=session_token.expires_in,
        id_token=session_token.id_token,
        access_token=session_token.access_token,
    )


@account_management_router.post(
    "/token", response_model=view_models.CreateTokenResponse
)
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session_token: SessionToken = account_management_service.login(
        form_data.username, form_data.password
    )
    return view_models.CreateTokenResponse(access_token=session_token.access_token)


@account_management_router.get(
    "/validate-oauth-token", response_model=view_models.ValidateTokenResponse
)
async def validate_oauth_token(access_token: str = Depends(oauth2_scheme)):
    return view_models.ValidateTokenResponse(access_token=access_token)
