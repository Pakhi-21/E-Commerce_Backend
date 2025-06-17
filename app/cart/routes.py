from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.cart import models, schemas
from app.utils.dependency import get_db, require_user
from app.products.models import Product
from app.cart.models import CartItem
import logging

logger = logging.getLogger("ecommerce_logger")

router = APIRouter(prefix="/cart", tags=["Cart"])

#view item of cart
@router.get("/", response_model=list[schemas.CartItemOut])
def view_cart(db: Session = Depends(get_db),user=Depends(require_user)):
    try:
        cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
        logger.info(f"Fetched cart items for user {user.id}")
        return cart_items
    except Exception as e:
        logger.error(f"Error viewing cart for user {user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while fetching the cart")

## add item in cart
@router.post("/", response_model=schemas.CartItemOut)
def add_to_cart(data: schemas.CartItemCreate,db: Session = Depends(get_db),user=Depends(require_user)):
    try:
        product = db.query(Product).filter_by(id=data.product_id).first()
        if not product:
            logger.warning("Add to cart failed - Product not found)")
            raise HTTPException(status_code=404, detail="Product not found")

        if (product.stock == 0):
            raise HTTPException(status_code=400, detail="Product is out of stock")
        
        #Checks if the item already exists 
        item = db.query(CartItem).filter_by(user_id=user.id, product_id=data.product_id).first()

        if (item):
            #update quantity.
            if item.quantity + data.quantity > product.stock:
                raise HTTPException(status_code=400, detail="Product is out of stock")
            item.quantity += data.quantity
            logger.info(f"Updated cart item quantity for user {user.id}")
        else:
            if (data.quantity > product.stock):
                raise HTTPException(status_code=400, detail="Product is out of stock")
            item = CartItem(user_id=user.id, **data.model_dump())
            db.add(item)
            logger.info(f"Added new item to cart for user {user.id}")

        db.commit()
        db.refresh(item)
        return item

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while adding to cart")


#update particular item quantity in a cart
@router.put("/{product_id}", response_model=schemas.CartItemOut)
def update_quantity(
    product_id: int,
    data: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    try:
        item = db.query(CartItem).filter_by(user_id=user.id, product_id=product_id).first()
        if not item:
            logger.warning(f"Update failed: Item not found in cart (User: {user.id}, Product: {product_id})")
            raise HTTPException(status_code=404, detail="Item not in cart")

        product = db.query(Product).filter_by(id=product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.quantity > product.stock:
            raise HTTPException(status_code=400, detail="Product is out of stock")

        item.quantity = data.quantity
        db.commit()
        db.refresh(item)
        logger.info(f"Updated quantity for cart item (User: {user.id}, Product: {product_id})")
        return item

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error updating quantity: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while updating the item")
    
## delete item from a cart
@router.delete("/{product_id}")
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_user)
):
    try:
        item = db.query(CartItem).filter_by(user_id=user.id, product_id=product_id).first()
        if not item:
            logger.warning(f"Remove failed: Item not found in cart Product: {product_id})")
            raise HTTPException(status_code=404, detail="Item not in cart")

        db.delete(item)
        db.commit()
        logger.info(f"Removed item from cart (User: {user.id}, Product: {product_id})")
        return {"message": "Product removed"}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error removing item from cart: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while removing the item")
