# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, Base, get_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# In-memory database to store items (for demonstration)
items_db = []

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Route to create an item.
    - item: Data required to create an item (name, description, price).
    - db: Database session for interacting with the database.
    """
    db_item = models.Item(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh the instance to get the ID
    return db_item

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Route to read an item by its ID.
    - item_id: The ID of the item to retrieve.
    - db: Database session for querying the database.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Route to read a list of items.
    - skip: Number of records to skip for pagination.
    - limit: Maximum number of records to return.
    - db: Database session for querying the database.
    """
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items
