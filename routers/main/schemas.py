from pydantic import BaseModel
from datetime import date

class ChatRequest(BaseModel):
    message: str

class RegisterSchema(BaseModel):
    number: str
    username: str
    password: str
    f_name: str
    l_name: str
    birthday_date: date
    