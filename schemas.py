from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


# class LoginCreate(BaseModel):
#     tp: str = Field(..., alias='typing_pattern')
#     custom_field: Optional[str] = Field(default=None)
#
#
# class LoginReturn(BaseModel):
#     action: str
#     custom_field: str
#     enrollment: bool
#     high_confidence: bool
#     message: str
#     message_code: int
#     result: bool
#     status: HTTPStatus


class LoginRequestSchema(BaseModel):
    email: EmailStr


class LoginResponseSchema(BaseModel):
    is_success: bool = Field(default=True)
    is_verified: bool = Field(default=True)
    email: EmailStr


class SignupRequestSchema(BaseModel):
    email: EmailStr


class SignupResponseSchema(BaseModel):
    is_success: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    email: EmailStr


class VerifyRequestSchema(BaseModel):
    email: EmailStr
    typing_pattern: str


class VerifyResponseSchema(BaseModel):
    pass