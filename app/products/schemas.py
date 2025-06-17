from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(..., gt=0, description="Price must be > 0")
    stock: int=Field(..., ge=0, description="Stock must be >= 0")
    category: str
    image_url: str

    #name validator
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if not (2 <= len(v) <= 100):
            raise ValueError("Name must be between 2 and 100 characters long")
        return v
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]):
        if v is not None and (len(v) < 2 or len(v) > 50):
            raise ValueError("Category must be between 2 and 50 characters")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0, description="Price must be > 0")
    stock: Optional[int] = Field(None, ge=0, description="Stock must be >= 0")
    category: Optional[str] = None
    image_url: Optional[str] = None

    #name validator
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if not (2 <= len(v) <= 100):
            raise ValueError("Name must be between 2 and 100 characters long")
        return v
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: Optional[str]):
        if v is not None and (len(v) < 2 or len(v) > 50):
            raise ValueError("Category must be between 2 and 50 characters")
        return v

class ProductOut(ProductBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }
