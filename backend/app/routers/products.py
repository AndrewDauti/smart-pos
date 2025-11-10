from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.post("/", response_model=schemas.ProductRead, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Product).filter_by(sku=product.sku).first()
    if exists:
        raise HTTPException(status_code=400, detail="SKU already exists")
    obj = models.Product(**product.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in product.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        return
    db.delete(obj)
    db.commit()
