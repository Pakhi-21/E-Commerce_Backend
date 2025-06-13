from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from app.utils.dependency import get_db, require_user
from app.cart.models import CartItem
from app.products.models import Product
from app.orders.models import Order, OrderItem, OrderStatus

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("/")
def checkout(db: Session = Depends(get_db), user=Depends(require_user)):
    try:
        cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Empty Cart")

        total = 0

        # Status initially set to pending
        order = Order(user_id=user.id, total_amount=0, status=OrderStatus.PENDING)
        db.add(order)
        db.flush()

        for item in cart_items:
            product = db.query(Product).filter_by(id=item.product_id).first()
            if not product or product.stock < item.quantity:
                raise HTTPException(status_code=400, detail="Product Out of Stock")

            product.stock -= item.quantity
            subtotal = item.quantity * product.price
            total += subtotal
            
            ## creating order in DB
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=product.name,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
            db.add(order_item)

        order.total_amount = total
        order.status = OrderStatus.PAID  # Update status after successful payment
        db.query(CartItem).filter_by(user_id=user.id).delete()
        db.commit()

        return {
            "Message": "Order Placed Successfully",
            "Order_id": order.id,
            "Total Amount": total,
            "Status": order.status.value
        }
    
    except HTTPException as http_exc:
         raise http_exc 
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Order not Placed: {str(e)}"
        )