from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, database
from pydantic import BaseModel

app = FastAPI(title="ARTIST API")

models.Base.metadata.create_all(bind=database.engine)

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    class Config:
        from_attributes = True

@app.post("/items/", response_model=ItemRead)
def create_item(item: ItemCreate, db: Session = Depends(database.get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(database.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", response_model=ItemRead)
def delete_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item

@app.get("/items/", response_model=list[ItemRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items
