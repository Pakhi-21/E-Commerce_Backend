from pydantic import BaseModel
from datetime import datetime


class OrderItemOut(BaseModel):
    product_id: int
    product_name: str  
    quantity: int
    price_at_purchase: float

    model_config = {
        "from_attributes": True
    }

class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: list[OrderItemOut]

    model_config = {
        "from_attributes": True
    }