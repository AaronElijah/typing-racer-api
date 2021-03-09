from http import HTTPStatus

from pydantic import BaseModel, Field, EmailStr


class LoginRequestSchema(BaseModel):
    email: EmailStr


class LoginResponseSchema(BaseModel):
    is_success: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    email: EmailStr


class SignupRequestSchema(BaseModel):
    email: EmailStr


class SignupResponseSchema(BaseModel):
    is_success: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    email: EmailStr


class VerifyRequestSchema(BaseModel):
    email: EmailStr
    typing_pattern: str


class VerifyResponseSchema(BaseModel):
    action: str
    custom_field: str
    enrollment: bool
    high_confidence: bool
    message: str
    message_code: int
    result: bool
    status: HTTPStatus
