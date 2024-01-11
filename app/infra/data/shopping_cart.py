from typing import Annotated

from pydantic import Field, ConfigDict
from bson.objectid import ObjectId

from entities import ShoppingCart
from .mongo_id import PyObjectId


class ShoppingCartModel(ShoppingCart):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    id: Annotated[ObjectId, PyObjectId] = Field(alias="_id", serialization_alias="id")
