from pydantic import Field
from pydantic_settings import BaseSettings

from .mongo_settings import MongoSettings
from .uvicorn import UvicornSettings


class ServerSettings(BaseSettings):
    """Server Settings"""

    uvicorn: UvicornSettings = Field(UvicornSettings())
    mongo: MongoSettings = Field(MongoSettings())


environment = ServerSettings()


if __name__ == "__main__":
    print(ServerSettings().model_dump())
