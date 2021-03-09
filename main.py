import json
import os
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import authorization
import temp
import words


os.environ['PYTHONHASHSEED'] = '0'

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    with open('words.json') as json_file:
        data = json.load(json_file)
        words = random.sample(data.items(), 1000)

        def remove_word_without_definitions(word):
            if word[1].get('definitions'):
                definitions = word[1].get('definitions')
                if definitions[0].get('definition') != '':
                    return True
            return False

        filtered_words = list(filter(remove_word_without_definitions, words))
        temp.words = filtered_words

app.include_router(
    authorization.authorization_router,
    tags=['Authorization'],
)
app.include_router(
    words.words_router,
    tags=['Words'],
)

origins = [
    'http://localhost',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

