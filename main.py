from fastapi import FastAPI
from enum import Enum
# from typing import Optional

app = FastAPI()

# @app.get("/")
# async def root():
#     return {'message': 'hello my world'}


@app.get("/")
# @app.get("/", description="this is base route")
# @app.get("/", description="this is base route", deprecated=True)
async def root():
    return {'message': 'hello my world'}


@app.post("/")
async def post():
    return {'message': 'hello my post world'}


@app.put("/{id}")
async def put():
    return {'message': "id"}


@app.get("/users")
async def list_users():
    return {'message': 'users list'}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {'user_id': user_id}


@app.get("/users/{user_id}")
async def get_user(user_id):
    return {'user_id': user_id}


@app.get("/users/me")
async def get_current_me():
    return {'user_id': "this is me"}


@app.get("/users/{user_id}")
async def list_users(user_id: int):
    return {'user_id': user_id}


class FoodEnum(str, Enum):
    fruits = 'fruits'
    vegetables = 'vegetables'
    dairy = 'dairy'

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": "this is vegetable category"}

    if food_name == FoodEnum.fruits:
        return {"food_name": "this is fruit category"}

    if food_name == FoodEnum.dairy:
        return {"food_name": "this is dairy category"}

    return {"food_name": "not able to process"}


@app.get("/items")
async def list_items(query):
    return {"data": query}


# @app.get("/items/{item_id}")
# async def get_item(item_id, query: int = 10):
#     if query:
#         return {"item_id": item_id, "data": query}

#     return {"data": query}


@app.get("/items/{item_id}")
async def get_item(item_id, query= None):
    if query:
        return {"item_id": item_id, "data": query}

    return {"item_id": item_id}


@app.get("/items/{item_id}/type/{user_id}")
async def get_item(user_id, item_id, query= None):
    if query:
        return {"item_id": item_id, "user_id": user_id, "data": query}

    return {"item_id": item_id, "user_id": user_id}
