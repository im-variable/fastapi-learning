from fastapi import FastAPI, Query, Path, Cookie, Header, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta, time

app = FastAPI()

# 4. Method and URL Creation
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}

# 5. URL Parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}

@app.get("/books/{book_id}")
async def read_book(book_id: Optional[int] = None):
    return {"book_id": book_id}

# 6. URL Parameter with Data Type (Pydantic)
class Item(BaseModel):
    name: str
    price: float

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

@app.get("/search/")
async def search_item(name: str, max_price: float):
    return {"name": name, "max_price": max_price}

# 7. Routing - URL Ordering
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "current_user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/admin")
async def read_admin():
    return {"role": "admin"}

@app.get("/users/{user_id}")
async def read_user_by_id(user_id: int):
    return {"user_id": user_id}

# 8. Enum with URL Parameter
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name}

class Role(str, Enum):
    admin = "admin"
    user = "user"

@app.get("/roles/{role}")
async def get_role(role: Role):
    return {"role": role}

# 9. Query Parameter
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/products/")
async def read_product(q: str):
    return {"query": q}

@app.get("/books/")
async def read_books(genre: Optional[str] = None):
    return {"genre": genre}

# 10. Use of BaseModel
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

@app.post("/users/")
async def create_user(user: User):
    return {"user": user}

# 11. FastAPI - Query Class
@app.get("/items/")
async def read_items_with_query(q: str = Query(None, min_length=3)):
    return {"q": q}

@app.get("/products/")
async def read_products(search: str = Query(..., alias="search_term", example="fastapi")):
    return {"search": search}

@app.get("/books/")
async def read_books_with_query(q: str = Query(None, max_length=50)):
    return {"q": q}

# 12. Other Parameter - Example, HttpUrl
class Product(BaseModel):
    image_url: HttpUrl

@app.post("/products/")
async def create_product(product: Product):
    return {"image_url": product.image_url}

# 13. Nested BaseModel
class SubItem(BaseModel):
    name: str
    description: str

class ComplexItem(BaseModel):
    name: str
    sub_item: SubItem

@app.post("/items/")
async def create_complex_item(item: ComplexItem):
    return item

class UserAddress(BaseModel):
    city: str
    state: str

class UserWithAddress(BaseModel):
    name: str
    address: UserAddress

@app.post("/users_with_address/")
async def create_user_with_address(user: UserWithAddress):
    return user

# 14. Extra Datatypes - UUID, datetime, timedelta, time
@app.post("/items/{item_id}")
async def create_item_with_uuid(item_id: UUID):
    return {"item_id": item_id}

class Event(BaseModel):
    start_time: datetime
    duration: timedelta

@app.post("/events/")
async def create_event(event: Event):
    return {"event": event}

class Meeting(BaseModel):
    meeting_time: time

@app.post("/meetings/")
async def create_meeting(meeting: Meeting):
    return {"meeting_time": meeting.meeting_time}

# 15. Cookies and Headers
@app.get("/items/")
async def read_items_with_cookies(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

@app.get("/headers/")
async def read_headers(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/info/")
async def get_info(ads_id: Optional[str] = Cookie(None), user_agent: Optional[str] = Header(None)):
    return {"ads_id": ads_id, "user_agent": user_agent}

# 16. Response - Response Model
@app.get("/items_response/", response_model=List[Item])
async def read_items_response():
    return [{"name": "Item 1", "price": 10.5}, {"name": "Item 2", "price": 15.0}]

class SubItemResponse(BaseModel):
    name: str

class ItemResponse(BaseModel):
    name: str
    sub_item: SubItemResponse

@app.get("/items_with_subitem/", response_model=ItemResponse)
async def read_item_with_subitem():
    return {"name": "Item 1", "sub_item": {"name": "SubItem 1"}}

# 17. Status Codes
@app.post("/items_with_status/", status_code=status.HTTP_201_CREATED)
async def create_item_with_status(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return {"item_id": item_id}

@app.put("/items_with_status/{item_id}", status_code=202)
async def update_item_with_status(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

# 18. Request Files
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/uploadfiles/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@app.post("/files/")
async def upload_file_and_data(file: UploadFile = File(...), description: str = Form(...)):
    return {"filename": file.filename, "description": description}

# 19. Error Handling
@app.get("/items/{item_id}")
async def read_item_with_error_handling(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

@app.get("/users/{user_id}")
async def read_user_with_error(user_id: str):
    if user_id != "admin":
        raise HTTPException(status_code=400, detail="Invalid user", headers={"X-Error": "Invalid"})
    return {"user_id": user_id}

@app.get("/books/{book_id}")
async def read_book_with_error(book_id: int):
    if book_id < 0:
        raise HTTPException(status_code=422, detail="Book ID must be positive")
    return {"book_id": book_id}
