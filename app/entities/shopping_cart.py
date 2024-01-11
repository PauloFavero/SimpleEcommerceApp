from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class CartItem(BaseModel):
    product_id: str
    quantity: int
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    @model_validator(mode="before")
    def handle_data_update(self):
        self.updated_at = datetime.now()


class ShoppingCart(BaseModel):
    user_id: str
    itens: list[CartItem] = []
    # updated_at: Field(default=datetime.now())
