from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cart import models, schemas
from app.utils.dependency import get_db, require_user
from app.products.models import Product

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/", response_model=schemas.CartItemOut)
def add_to_cart(
    data: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    product = db.query(Product).filter_by(id=data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=data.product_id).first()
    if item:
        item.quantity += data.quantity
    else:
        item = models.CartItem(user_id=user.id, **data.dict())
        db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=list[schemas.CartItemOut])
def view_cart(
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    return db.query(models.CartItem).filter_by(user_id=user.id).all()


@router.delete("/{product_id}")
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Products not in cart")
    db.delete(item)
    db.commit()
    return {"message": "Product removed"}


@router.put("/{product_id}", response_model=schemas.CartItemOut)
def update_quantity(
    product_id: int,
    data: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item

