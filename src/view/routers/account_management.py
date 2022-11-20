import json

import requests
from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from requests import Response  # type: ignore

import src.view.models as view_models

account_management_router = APIRouter(prefix="/users", tags=["users"])

with open("src/firebase-credentials.json") as credentials_file:
    CREDENTIALS = json.load(credentials_file)
API_KEY = CREDENTIALS["api_key"]


@account_management_router.post(
    "/create", response_model=view_models.CreateUserResponse
)
def create_user(payload: view_models.CreateUserPayload):
    user_record: auth.UserRecord = auth.create_user(
        email=payload.email, password=payload.password
    )
    return view_models.CreateUserResponse(email=user_record.email)


@account_management_router.post(
    "/login",
    response_model=view_models.LoginResponse,
    responses={403: {"description": "Authentication error."}},
)
def login(payload: view_models.LoginPayload):
    url: str = (
        f"https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        f"/verifyPassword?key={API_KEY}"
    )
    headers = {"content-type": "application/json; charset=UTF-8"}
    request_body = json.dumps(
        {
            "email": payload.email,
            "password": payload.password,
            "returnSecureToken": True,
        }
    )
    response: Response = requests.post(url, headers=headers, data=request_body)

    if not response.ok:
        raise HTTPException(status_code=403, detail="Authentication error.")

    response_json: dict = response.json()
    return view_models.LoginResponse(
        email=response_json["email"],
        expires_in=response_json["expiresIn"],
        id_token=response_json["idToken"],
        access_token=response_json["refreshToken"],
    )
