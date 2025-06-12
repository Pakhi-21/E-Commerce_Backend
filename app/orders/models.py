from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum as SqlEnum 
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.sql import func
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    total_amount = Column(Float)
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    product_name = Column(String)
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    order = relationship("Order", back_populates="items")
    


