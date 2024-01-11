from pydantic import BaseModel, field_validator


class Pagination(BaseModel):
    page: int
    limit: int
    pages: int
    total: int
