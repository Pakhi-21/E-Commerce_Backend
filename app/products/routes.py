from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.dependency import get_db, require_admin 
from app.products import schemas, models

router = APIRouter(prefix="/admin/products", tags=["Admin-Products"])



@router.post("/", response_model=schemas.ProductOut)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db), _ = Depends(require_admin)):
    product = models.Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=list[schemas.ProductOut])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _ = Depends(require_admin)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
    product = db.query(models.Product).filter_by(id=id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db), _ = Depends(require_admin)):
    product = db.query(models.Product).filter_by(id=id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
    product = db.query(models.Product).filter_by(id=id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
