from typing import Optional, Dict, Any
from datetime import datetime

from pydantic import Field
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from pymongo.database import Database
from pymongo.collection import Collection

from entities import User, UpdateUser
from ..handler import db as mongo_database
from infra import encrypt_password
from ...data.users import UserModel, PaginatedUsersModel
from ..helpers.pagination import build_pagination_query


class AddUserModel(User):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UsersRepository:
    def __init__(self, db: Database = mongo_database) -> None:
        self.__db: Database = db
        self.__collection: Collection = self.__db.get_collection("users")

    def get_all_users(self, page, limit) -> PaginatedUsersModel:
        pagination_stage = build_pagination_query(page, limit)
        pipeline = [{"$match": {}}] + pagination_stage
        users = list(self.__collection.aggregate(pipeline))[0]
        print(users)
        return PaginatedUsersModel(**users)

    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        return self.__collection.find_one({"_id": ObjectId(id)})

    def create_user(self, user: User) -> str:
        add_data = AddUserModel(**user.model_dump())
        add_data.password = encrypt_password(add_data.password)
        result = self.__collection.insert_one(add_data.model_dump())
        return str(result.inserted_id)

    def update_user(self, id: str, user: UpdateUser) -> bool:
        update_data: Dict[str, Any] = user.model_dump(exclude_none=True)
        password = update_data.get("password", None)
        if password:
            update_data["password"] = encrypt_password(password)
        update_data["updated_at"] = datetime.now()
        result: UpdateResult = self.__collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        return result.modified_count > 0 or result.matched_count > 0
    
    def replace_user_data(self, id: str, user: UpdateUser) -> bool:
        user_data = AddUserModel(**user.model_dump())
        user_data.password = encrypt_password(user_data.password)
        result: UpdateResult = self.__collection.replace_one(
            {"_id": ObjectId(id)}, 
            user_data.model_dump()
        )
        return result.modified_count > 0 or result.matched_count > 0

    def delete_user(self, id: str) -> bool:
        result = self.__collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
