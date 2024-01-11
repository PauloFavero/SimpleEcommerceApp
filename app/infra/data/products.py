from datetime import datetime
from typing import List, Annotated

from pydantic import BaseModel, Field, ConfigDict
from bson.objectid import ObjectId

from entities import Product, Pagination
from .mongo_id import PyObjectId


class ProductModel(Product):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    id: Annotated[ObjectId, PyObjectId] = Field(alias="_id", serialization_alias="id")
    created_at: datetime
    updated_at: datetime


class PaginatedProductsModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    data: List[ProductModel]
    pagination: Pagination
