# schemas.py
from pydantic import BaseModel

# Define how data is structured when creating a new item
class ItemCreate(BaseModel):
    name: str
    description: str
    price: int

# Define how data is structured when returning items
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True  # Enable reading from SQLAlchemy models
