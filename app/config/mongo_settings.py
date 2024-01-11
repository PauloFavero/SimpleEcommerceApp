from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class MongoSettings(BaseSettings):
    """Mongo Settings"""

    host: str = Field("db", validation_alias=AliasChoices("mongo_uri", "mongo_url"))
    port: int = Field(27017, alias="mongo_port")
    db: str = Field("ecomm", alias="mongo_db")
