from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Roles(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    name: str
    email: str
    password: str
    role: Roles = Roles.user


class UpdateUser(BaseModel):
    password: Optional[str] = None
    role: Optional[Roles] = None
