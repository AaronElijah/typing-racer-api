import base64
from hashlib import blake2b
from http import HTTPStatus
from typing import Dict

import requests

import constants
import temp
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


@authorization_router.post('/login', response_model=LoginResponseSchema)
def login(
    login_data: LoginRequestSchema = Body(...),
) -> LoginResponseSchema:
    email = login_data.email
    user_info = next(filter(lambda info: info.get('email') == email, temp.users), None)
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
    if email in temp.users:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conflict: user already exists',
        )
    temp.users.append({'email': email, 'is_verified': False})

    return SignupResponseSchema(is_success=True, email=email, is_verified=False)

# 02fd6d666565e585ac4ad4967e139b0d56c9672dde8e7d151774a9ec1bec926c7de03085fa5e5a1e7fd85f6c17959b27b1d5a4287dd05825d776e8faa9a11728 - use this as test email from aaronzakelijah@googlemail.com
# delete this user occasionally
@authorization_router.post('/verify')
def verify(
    verify_data: VerifyRequestSchema = Body(...),
) -> Dict:
    user_info = next(filter(lambda info: info.get('email') == verify_data.email, temp.users), None)
    if not user_info:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Not found: user nonexistent',
        )

    auth_string = f'{constants.api_key}:{constants.secret_key}'
    base64_auth_string = base64.encodebytes(auth_string.encode()).decode().replace('\n', '')

    headers = {
        'Authorization': f'Basic {base64_auth_string}',
    }
    email = verify_data.email
    hashed_email = blake2b(email.encode('utf-8')).hexdigest()

    url = f'{constants.base_url}/auto/{hashed_email}'
    print(hashed_email)

    data = {'tp': verify_data.typing_pattern}

    r = requests.post(
        url=url,
        headers=headers,
        data=data
    )

    response = r.json()
    if response.get('action').find('verify') >= 0:
        def set_verified_email(info):
            if info.get('email') == email:
                info['is_verified'] = True
            return info
        temp.users = list(map(set_verified_email, temp.users))

    return response



