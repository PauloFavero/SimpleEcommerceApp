from pydantic import BaseModel


class Category(BaseModel):
    parent_code: str
    name: str
    desc: str
    code: str
