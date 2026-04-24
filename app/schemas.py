from pydantic import BaseModel
from typing import Optional, List


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    created_at: Optional[str] = None


class AddToCartSchema(BaseModel):
    cart_id: str
    product_id: str
    quantity: int


class CartItemResponse(BaseModel):
    item_id: str
    product_id: str
    product_name: str
    product_price: float
    quantity: int


class CartResponse(BaseModel):
    cart_id: str
    items: List[CartItemResponse]


class OrderResponse(BaseModel):
    order_id: str
    total: float
    payment: str