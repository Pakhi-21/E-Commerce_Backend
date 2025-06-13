from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.dependency import require_user, get_db
from app.orders import models, schemas
import logging

logger = logging.getLogger("ecommerce_logger")

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[schemas.OrderOut])
def order_history(db: Session = Depends(get_db), user=Depends(require_user)):

    try:
        orders = db.query(models.Order).filter_by(user_id=user.id).all()
        logger.info(f"Fetched order history for user {user.id}")
        return orders
    
    except Exception as e:

        logger.error(f"Error : fetching order history for user: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while fetching order history")


@router.get("/{order_id}", response_model=schemas.OrderOut)
def order_detail(order_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    try:
        order = db.query(models.Order).filter_by(id=order_id, user_id=user.id).first()

        if not order:
            logger.warning(f"Order not found (User: {user.id}, Order ID: {order_id})")
            raise HTTPException(status_code=404, detail="Order not found")

        logger.info(f"Fetched order details (User: {user.id}, Order ID: {order_id})")
        return order
    
    except HTTPException as http_exc:
         raise http_exc
    
    except Exception as e:
        logger.error(f"Error fetching order details for user {user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong while fetching order details")