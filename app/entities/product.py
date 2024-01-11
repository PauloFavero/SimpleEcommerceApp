from typing import Optional
from pydantic import BaseModel, Field, model_validator

from .product_characterists import Colors


class Product(BaseModel):
    name: str
    desc: str
    sku: str
    price: float
    stock_quantity: int
    color: Colors = Colors.BLACK
    category_id: str
    image: str


class UpdateProduct(BaseModel):
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    color: Optional[Colors] = None
    image: Optional[str] = None
