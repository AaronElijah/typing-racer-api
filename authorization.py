import base64
from http import HTTPStatus
from typing import Dict

import requests

import constants
import temp_db
from fastapi import Body, HTTPException, APIRouter
from schemas import (
    LoginCreate,
    LoginReturn,
    SignupCreate,
)


authorization_router = APIRouter()

@authorization_router.post('/login')
def login(
    login_data: LoginCreate = Body(...),
) -> LoginReturn:
    _id = login_data.custom_field
    if not _id or _id not in temp_db.users:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Unauthenticated: please sign up',
            headers={'Access-Control-Allow-Origin': '*'},
        )

    auth_string = f'{constants.api_key}:{constants.secret_key}'
    base64_auth_string = base64.encodebytes(auth_string.encode()).decode().replace('\n', '')

    headers = {
        'Authorization': f'Basic {base64_auth_string}',
    }
    data = login_data.dict(exclude={'custom_field'})
    url = f'{constants.base_url}/auto/{login_data.custom_field}'

    r = requests.post(
        url,
        headers=headers,
        data=data,
    )

    return r.json()


@authorization_router.post('/signup')
def signup(
    signup_data: SignupCreate = Body(...),
) -> Dict:
    print(signup_data)

    return {'Hello': 'World'}