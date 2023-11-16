from typing_extensions import Unpack
from pydantic import BaseModel
from typing import Optional


class Account(BaseModel):
    id: str
    name: str
    email: str
    cpf: str
    car_plate: Optional[str]
    is_passenger: bool
    is_driver: bool
    password: str


class AccountCreate(BaseModel):
    name: str
    email: str
    cpf: str
    car_plate: Optional[str]
    is_passenger: bool
    is_driver: bool
    password: str
