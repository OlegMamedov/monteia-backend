from pydantic import BaseModel, validator
from datetime import date

class ChatRequest(BaseModel):
    message: str

class RegisterSchema(BaseModel):
    number: str
    f_name: str
    l_name: str
    birthday_date: date

    @validator('number')
    def validate_number(cls, v):
        if not v.startswith('7'):
            raise ValueError('Number must start with 7')
        if len(v) != 11:
            raise ValueError('Number must be 11 characters long')
        return v

class LoginSchema(BaseModel):
    number: str

    @validator('number')
    def validate_number(cls, v):
        if not v.startswith('7'):
            raise ValueError('Number must start with 7')
        if len(v) != 11:
            raise ValueError('Number must be 11 characters long')
        return v

class AuthSchema(BaseModel):
    number: str
    code: str

    @validator('number')
    def validate_number(cls, v):
        if not v.startswith('7'):
            raise ValueError('Number must start with 7')
        if len(v) != 11:
            raise ValueError('Number must be 11 characters long')
        return v

class GadanieSchema(BaseModel):
    pass
