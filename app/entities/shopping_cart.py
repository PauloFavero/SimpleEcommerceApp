from typing import List, Optional
from pydantic import BaseModel


class CartItem(BaseModel):
    product_id: str
    quantity: int

class ShoppingCart(BaseModel):
    user_id: str
    items: List[Optional[CartItem]] = []
