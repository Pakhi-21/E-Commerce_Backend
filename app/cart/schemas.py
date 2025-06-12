from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: int=Field(..., gt=0, description="Product ID must be positive")
    quantity: int=Field(..., gt=0, description="Quantity must be > 0")

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int=Field(..., gt=0, description="Quantity must be > 0")

class CartItemOut(CartItemBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }