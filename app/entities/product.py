from datetime import datetime

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
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    @model_validator(mode="before")
    def handle_data_update(self):
        self.updated_at = datetime.now()
