from typing import Optional, Dict, Any, List
from datetime import datetime

from pydantic import Field
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from pymongo.database import Database
from pymongo.collection import Collection

from ..handler import db as mongo_database
from ...data import ShoppingCartModel
from entities import ShoppingCart, CartItem


class ShoppingCartRepository:
    def __init__(self, db: Database = mongo_database) -> None:
        self.__db: Database = db
        self.__collection: Collection = self.__db.get_collection("shoppingCart")

    def create_shopping_cart(self, user_id: str) -> str:
        data = ShoppingCart(user_id=user_id)
        result = self.__collection.insert_one(data.model_dump())
        return str(result.inserted_id)

    def get_shopping_cart_by_id(self, id: str) -> Optional[ShoppingCartModel]:
        cart = self.__collection.find_one({"_id": ObjectId(id)})
        print('mongo get_shopping_cart_by_id', cart)
        return ShoppingCartModel(**cart) if cart else None
    
    def get_shopping_cart_by_user_id(self, user_id: str) -> Optional[ShoppingCartModel]:
        cart = self.__collection.find_one({"user_id": ObjectId(user_id)})
        return ShoppingCartModel(**cart) if cart else None  

    def add_items(self, id: str, cart_item: List[CartItem]) -> bool:
        items_to_add = [item.model_dump() for item in cart_item]
        result: UpdateResult = self.__collection.update_one(
            {"_id": ObjectId(id)}, {"$push": { "items": { "$each": items_to_add} }}
        )
        return result.modified_count > 0 or result.matched_count > 0

    def remove_items(self, id: str, cart_items: List[str]) -> bool:
        result: UpdateResult = self.__collection.update_one(
            {"_id": ObjectId(id)}, {"$pull": { "items": { "product_id": { "$in": cart_items } } }}
        )
        return result.modified_count > 0 or result.matched_count > 0

    def clear_cart(self, id: str) -> None:
        result: UpdateResult = self.__collection.update_one(
            {"_id": ObjectId(id)}, {"$set": { "items": [] }}
        )
        return result.modified_count > 0 or result.matched_count > 0
    
    def delete_shopping_cart(self, id: str) -> bool:
        result = self.__collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
