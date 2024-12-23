from fastapi import APIRouter, Depends, HTTPException, Path
from schemas import UserCreate
from models import Users
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db
from utilities import get_current_user, create_access_token, SECRET_KEY, ALGORITHM, oauth2_scheme, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette import status
from passlib.context import CryptContext

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

def get_user(db, email: str):
    user = db.query(Users).filter(Users.email==email).first()
    if user:
        return user
    return None

def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post('/create/')
async def create_user(db: db_dependency, create_user_request: UserCreate):
    # for password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    create_user = Users(first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        phone_no=create_user_request.phone_no,
        email=create_user_request.email,
        hashed_password=pwd_context.hash(create_user_request.password),
        is_active=True,
        middle_name=create_user_request.middle_name
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user

# @router.get('')
# async def user_list(db: db_dependency):
#     user_list = db.query(Users).all()
#     return user_list


@router.get("")
async def user_list(user: user_dependency, db: db_dependency):
    user_list = db.query(Users).all()
    return user_list


@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm , Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_obj = get_user(db, user)
        if user_obj is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_obj
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
