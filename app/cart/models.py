from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CartItem(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer, nullable=False)
