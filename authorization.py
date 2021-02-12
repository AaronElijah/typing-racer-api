import base64
from http import HTTPStatus
from typing import Dict

import requests

import constants
import temp_db
from auth_utils import get_hash
from fastapi import Body, HTTPException, APIRouter
from schemas import (
    LoginRequestSchema,
    LoginResponseSchema,
    SignupRequestSchema,
    SignupResponseSchema,
    VerifyRequestSchema,
    VerifyResponseSchema,
)


authorization_router = APIRouter()


# @authorization_router.post('/login')
# def login(
#     login_data: LoginCreate = Body(...),
# ) -> LoginReturn:
#     _id = login_data.custom_field
#     if not _id or _id not in temp_db.users:
#         raise HTTPException(
#             status_code=HTTPStatus.FORBIDDEN,
#             detail='Unauthenticated: please sign up',
#             headers={'Access-Control-Allow-Origin': '*'},
#         )
#
#     auth_string = f'{constants.api_key}:{constants.secret_key}'
#     base64_auth_string = base64.encodebytes(auth_string.encode()).decode().replace('\n', '')
#
#     headers = {
#         'Authorization': f'Basic {base64_auth_string}',
#     }
#     data = login_data.dict(exclude={'custom_field'})
#     url = f'{constants.base_url}/auto/{login_data.custom_field}'
#
#     r = requests.post(
#         url,
#         headers=headers,
#         data=data,
#     )
#
#     return r.json()


@authorization_router.post('/login', response_model=LoginResponseSchema)
def login(
    login_data: LoginRequestSchema = Body(...),
) -> LoginResponseSchema:
    email = login_data.email
    user_info = next(filter(lambda info: info.get('email') == email, temp_db.users), None)
    if not user_info:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Not found: user nonexistent',
        )
    is_verified = False
    if user_info.get('is_verified'):
        is_verified = True

    return LoginResponseSchema(is_success=True, email=email, is_verified=is_verified)


@authorization_router.post('/signup', response_model=SignupResponseSchema)
def signup(
    signup_data: SignupRequestSchema = Body(...),
) -> SignupResponseSchema:
    email = signup_data.email
    if email in temp_db.users:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conflict: user already exists',
        )
    temp_db.users.append({'email': email, 'is_verified': False})

    return SignupResponseSchema(is_success=True, email=email, is_verified=False)


@authorization_router.post('/verify')
def verify(
    verify_data: VerifyRequestSchema = Body(...),
) -> Dict:
    # We want the user email and typing pattern
    # When we submit the user email (hashed) and typing pattern, we should get either a verify, enroll or verify enroll
    # I think we can filter for the results that we don't need in the repsonse from typingDNA

    auth_string = f'{constants.api_key}:{constants.secret_key}'
    base64_auth_string = base64.encodebytes(auth_string.encode()).decode().replace('\n', '')

    headers = {
        'Authorization': f'Basic {base64_auth_string}',
    }
    hashed_email = get_hash(verify_data.email.encode('utf-8'))
    url = f'{constants.base_url}/auto/{hashed_email}'

    data = verify_data.dict(include={'typing_pattern'})

    r = requests.post(
        url=url,
        headers=headers,
        data=data
    )

    print(r.json())

    return {'Hello': 'World'}



