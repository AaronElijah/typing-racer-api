import threading
import functools
from typing import Any, Callable, Dict, Tuple
import concurrent.futures


import boto3
from mypy_boto3_dynamodb.service_resource import Table


def inject_threaded_db(func):
    @functools.wraps(func)
    def thread_wrapper(*args, **kwargs):
        def table_session_wrapper(*args, **kwargs):
            session = boto3.session.Session(
                profile_name='mfa',
            )
            dynamo_table: Table = session.resource('dynamodb', region_name='eu-west-2').Table('typingRacerDB')
            kwargs['db'] = dynamo_table
            return func(*args, **kwargs)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(table_session_wrapper, *args, **kwargs)
            response = future.result(timeout=10)
            return response

    return thread_wrapper
