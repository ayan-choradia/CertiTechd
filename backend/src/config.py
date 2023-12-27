import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

# from eth_account.signers.local import LocalAccount
from pydantic import AnyHttpUrl, AnyUrl, HttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DOMAIN: AnyHttpUrl
    RELOAD: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    ALGORITHM: str = "HS256"
    MSSQL_SERVER: str
    MSSQL_USER: str
    MSSQL_PASSWORD: str
    MSSQL_DB: str
    MSSQL_PORT: int
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    DEBUG: bool

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        server = values.get("MSSQL_SERVER")
        database = values.get("MSSQL_DB")
        username = values.get("MSSQL_USER")
        password = values.get("MSSQL_PASSWORD")
        port = values.get("MSSQL_PORT")
        encoded_password = quote(password, safe="")

        connection_string = f"mssql+pyodbc://{username}:{encoded_password}@{server}:{port}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
        return connection_string

    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
