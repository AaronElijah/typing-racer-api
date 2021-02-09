from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class LoginCreate(BaseModel):
    tp: str = Field(..., alias='typing_pattern')
    custom_field: Optional[str] = Field(default=None)


class LoginReturn(BaseModel):
    action: str
    custom_field: str
    enrollment: bool
    high_confidence: bool
    message: str
    message_code: int
    result: bool
    status: HTTPStatus


class SignupCreate(BaseModel):
    email: EmailStr
    name: str
    username: str
    typing_patterns: str

