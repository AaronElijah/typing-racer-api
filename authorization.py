import base64
import threading
from hashlib import blake2b
from http import HTTPStatus

import requests

import auth_utils
import constants
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
    db = auth_utils.read_users_from_db()

    print('********')
    print('Old db')
    print(db)
    print('********')
    user_from_db = auth_utils.read_user_from_db(user_email=login_data.email)
    print(user_from_db)
    print('********')


    # We can replace with call to db
    user_info = next(filter(lambda info: info.get('email') == email, db), None)


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
    db = auth_utils.read_users_from_db()

    print('********')
    print('Old db')
    print(db)
    print('********')
    user_from_db = auth_utils.read_user_from_db(user_email=signup_data.email)
    print(user_from_db)
    print('********')

    db_emails = map(lambda user_info: user_info.get('email'), db)
    if email in db_emails:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conflict: user already exists',
        )
    new_user = {'email': email, 'is_verify': False}
    auth_utils.write_new_user_to_db_old(new_user=new_user)

    print('*******')
    print('Write to dynamodb')
    response = auth_utils.write_new_user_to_db(new_user=new_user)
    print(response)
    print('*******')

    return SignupResponseSchema(is_success=True, email=email, is_verified=False)


@authorization_router.post('/verify')
def verify(
    verify_data: VerifyRequestSchema = Body(...),
) -> VerifyResponseSchema:
    db = auth_utils.read_users_from_db()

    print('********')
    print('Old db')
    print(db)
    print('********')
    user_from_db = auth_utils.read_user_from_db(user_email=verify_data.email)
    print(user_from_db)
    print('********')

    user_info = next(filter(lambda info: info.get('email') == verify_data.email, db), None)
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

    data = {'tp': verify_data.typing_pattern}

    r = requests.post(
        url=url,
        headers=headers,
        data=data
    )

    response = r.json()

    print(threading.current_thread().ident)
    if response.get('action'):
        action = response.get('action')
        if action.find('verify') >= 0:
            auth_utils.update_verification(email=email, is_verified=True)

    return response



