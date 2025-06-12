from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.utils.dependency import get_db, require_user
from app.cart.models import CartItem
from app.products.models import Product
from app.orders.models import Order, OrderItem

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("/")
def checkout(db: Session = Depends(get_db), user=Depends(require_user)):
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Empty cart")

    total = 0
    order = Order(user_id=user.id, total_amount=0)
    db.add(order)
    db.flush()

    for item in cart_items:
        product = db.query(Product).filter_by(id=item.product_id).first()
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Out of Stock")

        product.stock -= item.quantity
        subtotal = item.quantity * product.price
        total += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=product.price
        )
        db.add(order_item)

    order.total_amount = total
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()

    return {"message": "Order placed successfully", "order_id": order.id, "total": total}


