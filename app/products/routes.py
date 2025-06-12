from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.dependency import get_db, require_admin 
from app.products import schemas, models

import logging


logger = logging.getLogger("ecommerce_logger")

router = APIRouter(prefix="/admin/products", tags=["Admin-Products"])



# @router.post("/", response_model=schemas.ProductOut)
# def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db), _ = Depends(require_admin)):
#     product = models.Product(**data.model_dump())
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product

# @router.get("/", response_model=list[schemas.ProductOut])
# def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _ = Depends(require_admin)):
#     return db.query(models.Product).offset(skip).limit(limit).all()

# @router.get("/{id}", response_model=schemas.ProductOut)
# def get_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
#     product = db.query(models.Product).filter_by(id=id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# @router.put("/{id}", response_model=schemas.ProductOut)
# def update_product(id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db), _ = Depends(require_admin)):
#     product = db.query(models.Product).filter_by(id=id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     update_data = data.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(product, key, value)
        
#     db.commit()
#     db.refresh(product)
#     return product


# @router.delete("/{id}")
# def delete_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
#     product = db.query(models.Product).filter_by(id=id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     db.delete(product)
#     db.commit()
#     return {"message": "Product deleted"}


@router.post("/", response_model=schemas.ProductOut)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db), _ = Depends(require_admin)):
    try:
        product = models.Product(**data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"Product created with ID: {product.id}")
        return product
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        logger.error(f"Failed to create product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create product")


@router.get("/", response_model=list[schemas.ProductOut])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _ = Depends(require_admin)):
    try:
        products = db.query(models.Product).offset(skip).limit(limit).all()
        logger.info("Fetched all products")
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")



@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
    try:
        product = db.query(models.Product).filter_by(id=id).first()
        if not product:
            logger.warning(f"Product with ID {id} not found")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info(f"Fetched product with ID: {id}")
        return product
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        logger.error(f"Error fetching product {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")


@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db), _ = Depends(require_admin)):
    try:
        product = db.query(models.Product).filter_by(id=id).first()
        if not product:
            logger.warning(f"Product with ID {id} not found for update")
            raise HTTPException(status_code=404, detail="Product not found")
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        logger.info(f"Product with ID {id} updated")
        return product
    
    except HTTPException as http_exc:
         raise http_exc
     
    except Exception as e:
        logger.error(f"Failed to update product {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update product")


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db), _ = Depends(require_admin)):
    try:
        product = db.query(models.Product).filter_by(id=id).first()
        if not product:
            logger.warning(f"Product with ID {id} not found for deletion")
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product)
        db.commit()
        logger.info(f"Product with ID {id} deleted")
        return {"message": "Product deleted"}
    
    except HTTPException as http_exc:
         raise http_exc 
    
    except Exception as e:
        logger.error(f"Failed to delete product {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete product")