from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Address(BaseModel):
    user_id: str
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    phone: str
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    @model_validator(mode="before")
    def handle_data_update(self):
        self.updated_at = datetime.now()
