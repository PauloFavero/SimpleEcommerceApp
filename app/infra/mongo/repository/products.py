from typing import Optional, Dict, Any, List
from datetime import datetime

from pydantic import Field
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ASCENDING, DESCENDING

from entities import Product, UpdateProduct
from ..handler import db as mongo_database
from ...data.products import ProductModel, PaginatedProductsModel
from ..helpers.pagination import build_pagination_query


class AddProductModel(Product):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProductsRepository:
    def __init__(self, db: Database = mongo_database) -> None:
        self.__db: Database = db
        self.__collection: Collection = self.__db.get_collection("products")

    def get_all_products(
        self,
        page: int = 1,
        limit: int = 10,
        sort_order: int = 1,
        sort_by: str = "name",
        category_filter: str = None,
    ) -> PaginatedProductsModel:
        pipeline: List[Dict[str, Any]] = []
        if category_filter:
            pipeline.append({"$match": {"category": category_filter}})
        else:
            pipeline.append({"$match": {}})
        if sort_order == 1:
            pipeline.append({"$sort": {sort_by: ASCENDING}})
        else:
            pipeline.append({"$sort": {sort_by: DESCENDING}})
        pagination_stage = build_pagination_query(page, limit)
        pipeline += pagination_stage
        products = list(self.__collection.aggregate(pipeline))[0]
        return PaginatedProductsModel(**products)

    def get_product_by_id(self, id: str) -> Optional[ProductModel]:
        product = self.__collection.find_one({"_id": ObjectId(id)})
        return ProductModel(**product) if product else None

    def create_product(self, product: Product) -> str:
        add_data = AddProductModel(**product.model_dump())
        result = self.__collection.insert_one(add_data.model_dump())
        return str(result.inserted_id)

    def update_product(self, id: str, product: UpdateProduct) -> bool:
        update_data: Dict[str, Any] = product.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.now()
        result: UpdateResult = self.__collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        return result.modified_count > 0 or result.matched_count > 0

    def replace_product_data(self, id: str, product: UpdateProduct) -> bool:
        product_data = AddProductModel(**product.model_dump())
        result: UpdateResult = self.__collection.replace_one(
            {"_id": ObjectId(id)}, product_data.model_dump()
        )
        return result.modified_count > 0 or result.matched_count > 0

    def delete_product(self, id: str) -> bool:
        result = self.__collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
