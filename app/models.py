# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

# SQLAlchemy model for the 'items' table
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    user = Column(Integer, ForeignKey("users.id"))

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_no = Column(String)
    middle_name = Column(String)
