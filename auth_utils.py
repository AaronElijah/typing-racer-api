import bcrypt
import csv
from typing import Dict
import threading

import boto3

from db_utils import inject_threaded_db
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import PutItemOutputTypeDef, GetItemOutputTypeDef, UpdateItemOutputTypeDef


def get_hash(plain_text_password):
    # Hash a password for the first time
    # (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_hashed(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


def read_users_from_db():
    users = []
    with open('demo_db.csv', 'r', newline='') as db:
        reader = csv.reader(db, delimiter=' ')
        for row in reader:
            if row:
                user = {'email': row[0], 'is_verified': row[1]}
                users.append(user)
    db.close()
    return users


# def read_user_from_db(*, user_email: str) -> None:
#     with DBSingleThreadSession() as dynamodb_table:
#         response = dynamodb_table.get_item(
#             Key={
#                 'email': user_email,
#             },
#             ConsistentRead=False,
#             ReturnConsumedCapacity='TOTAL',
#         )
#         print(response.get('Item'))
#     return response.get('Item')

def write_new_user_to_db_old(new_user):
    with open('demo_db.csv', 'a', newline='') as db:
        writer = csv.writer(db, delimiter=' ')
        writer.writerow(new_user)
    db.close()


@inject_threaded_db
def write_new_user_to_db(*, new_user: Dict, **kwargs) -> PutItemOutputTypeDef:
    db: Table = kwargs['db']
    response: PutItemOutputTypeDef = db.put_item(
        Item={
            'email': new_user.get('email'),
            'is_verify': new_user.get('is_verify', False),
        },
        ReturnValues='ALL_OLD',
        ReturnConsumedCapacity='TOTAL',
        ReturnItemCollectionMetrics='SIZE',
    )
    print(threading.current_thread().ident)
    return response


@inject_threaded_db
def read_user_from_db(*, user_email: str, **kwargs) -> GetItemOutputTypeDef:
    db: Table = kwargs['db']
    response: GetItemOutputTypeDef = db.get_item(
        Key={
            'email': user_email,
        },
        ConsistentRead=False,
        ReturnConsumedCapacity='TOTAL',
    )
    print(threading.current_thread().ident)
    return response


@inject_threaded_db
def update_verification(
    *,
    email: str,
    is_verified: bool,
    **kwargs,
) -> UpdateItemOutputTypeDef:
    db: Table = kwargs['db']

    response: UpdateItemOutputTypeDef = db.update_item(
        Key={
            'email': email,
        },
        UpdateExpression='SET is_verified = :is_verified_value',
        ExpressionAttributeValues={
            ':is_verified_value': is_verified,
        },
        ReturnValues='UPDATED_NEW',
        ReturnItemCollectionMetrics='SIZE',
        ReturnConsumedCapacity='TOTAL',
    )
    print(threading.current_thread().ident)
    return response



def write_all_users_to_db(users):
    with open('demo_db.csv', 'w', newline='') as db:
        writer = csv.writer(db, delimiter=' ')
        writer.writerows(users)
    db.close()
