from enum import Enum
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, model_validator

from .payment import PaymentMethod


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class Order(BaseModel):
    user_id: str
    address_id: str
    itens: List[OrderItem] = []
    total: float = 0.0
    payment_method: PaymentMethod = PaymentMethod.credit_card
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    @model_validator(mode="before")
    def handle_data_update(self):
        self.updated_at = datetime.now()
