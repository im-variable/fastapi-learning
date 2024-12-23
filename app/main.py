from fastapi import FastAPI
from routers import items
from database import Base
from routers import auth, items
from database import engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(items.router, prefix='', tags=['items'])


