from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from typing import Annotated
from starlette import status

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

# router.dependency_overrides[get_db] = mock_get_db

@router.post("/items/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(db: db_dependency, item: schemas.ItemCreate):
    """
    Route to create an item.
    - item: Data required to create an item (name, description, price).
    - db: Database session for interacting with the database.
    """
    db_item = models.Items(**item.model_dump())
    # db_item = models.Item(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh the instance to get the ID
    return db_item

@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(db: db_dependency, item_id: int = Path(gt=0)):
    """
    Route to read an item by its ID.
    - item_id: The ID of the item to retrieve.
    - db: Database session for querying the database.
    """
    db_item = db.query(models.Items).filter(models.Items.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    # 1. Retrieve the existing item
    db_item = db.query(models.Items).filter(models.Items.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 2. Update only the provided fields
    update_data = item.model_dump(exclude_unset=True)  # Exclude unset fields
    for key, value in update_data.items():
        setattr(db_item, key, value)

    # 3. Save changes to the database
    db.commit()
    db.refresh(db_item)

    return db_item


@router.get("/items/", response_model=list[schemas.Item])
def read_items(db: db_dependency, skip: int = 0, limit: int = 10):
    """
    Route to read a list of items.
    - skip: Number of records to skip for pagination.
    - limit: Maximum number of records to return.
    - db: Database session for querying the database.
    """
    items = db.query(models.Items).offset(skip).limit(limit).all()
    return items

@router.delete("/items/{item_id}")
def delete_item(db: db_dependency, item_id: int):
    """
    - item_id: The ID of the item to retrieve.        
    - db: Database session for querying the database.
    """
    item = db.query(models.Items).filter(models.Items.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"detail": f"Item with ID {item_id} has been deleted."}
