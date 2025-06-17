from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.utils.dependency import get_db
from app.products.models import Product
from app.products.schemas import ProductOut
from typing import Literal, Optional
import logging

logger = logging.getLogger("ecommerce_logger")
router = APIRouter(prefix="/products", tags=["Public-Products"])

## Public endpoint to list all products with optional filters
@router.get("/", response_model=list[ProductOut])
def list_products(
    category: Optional[str] = None,
    min_price: float = 0,
    max_price: Optional[float] = None,
    sort_by: Optional[Literal["price", "name"]] = Query(None, description="Sort by 'price' or 'name' only"),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(func.lower(Product.category).like(f"%{category.lower()}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "name":
        query = query.order_by(Product.name)

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()


#view products by keyword in name or description.
@router.get("/search", response_model=list[ProductOut])
def search_products(keyword: str = Query(..., min_length=1),db: Session = Depends(get_db)):
    logger.info(f"Searching products with keyword: {keyword}")
    keyword = keyword.lower()
    query = db.query(Product).filter(
        or_(
            func.lower(Product.name).like(f"%{keyword}%"),
            func.lower(Product.description).like(f"%{keyword}%")
        )
    )
    
    return query.all()

##public endpoints to view product
@router.get("/{id}", response_model=ProductOut)
def get_product_detail(id: int, db: Session = Depends(get_db)):

    logger.info(f"Fetching product with ID: {id}")
    product = db.query(Product).filter_by(id=id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

