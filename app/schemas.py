# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# Define how data is structured when creating a new item
class ItemCreate(BaseModel):
    name: str = Field(min_length=4, max_length=250)
    description: str
    price: int

# Define how data is structured when returning items
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        # orm_mode = True  # Enable reading from SQLAlchemy models
        from_attributes = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_no: str
    middle_name: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    phone_no: str
    is_active: bool

