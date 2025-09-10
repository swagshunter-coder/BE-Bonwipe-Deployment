from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import ConfigDict

# ========== User ==========
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: str
    password: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        model_config = ConfigDict(from_attributes=True)
        
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# ========== Category ==========
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


# ========== Product ==========
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    stock: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    category: Category  # include nested category info

    class Config:
        model_config = ConfigDict(from_attributes=True)

class ProductOut(ProductBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


# ==== Bank ====
class BankBase(BaseModel):
    name: str
    account_number: str

class BankCreate(BankBase):
    pass

class BankOut(BankBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


# ========== Order item ==========
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(OrderItemCreate):
    id: int
    price_at_order: float

    class Config:
        model_config = ConfigDict(from_attributes=True)

# ========== Order ==========
class OrderCreate(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: str
    shipping_address: str
    bank_id: int
    transfer_proof: Optional[str] = None
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_email: Optional[str]
    customer_phone: str
    shipping_address: str
    transfer_proof: Optional[str]
    status: str
    created_at: datetime
    bank: BankOut  
    items: List[OrderItemOut]

    class Config:
        model_config = ConfigDict(from_attributes=True)

# ========== Tambahan ==========
class OrderDetailOut(OrderOut):
    total: float

class OrderStatusUpdate(BaseModel):
    status: str

