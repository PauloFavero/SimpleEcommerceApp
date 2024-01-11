from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class UvicornSettings(BaseSettings):
    """Uvicorn Settings"""

    host: str = Field(
        "localhost",
        validation_alias=AliasChoices("host", "server_host", "uvicorn_host"),
    )
    port: int = Field(
        8000, validation_alias=AliasChoices("port", "server_port", "uvicorn_port")
    )
    reload: bool = Field(
        False,
        validation_alias=AliasChoices("reload", "server_reload", "uvicorn_reload"),
    )
    log_level: str = Field(
        "info",
        validation_alias=AliasChoices(
            "log_level", "server_log_level", "uvicorn_log_level"
        ),
    )
    api_version: str = Field("1.0.0", alias="api_version")
