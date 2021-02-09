from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import authorization

app = FastAPI()


app.include_router(
    authorization.authorization_router,
    tags=['Authorization'],
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

