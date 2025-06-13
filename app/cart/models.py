from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
     
    product = relationship("Product", back_populates="cart_items") 