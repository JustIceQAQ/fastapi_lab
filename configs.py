from pydantic import BaseSettings


class Settings(BaseSettings):
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_CALLBACK_URL: str
    YAHOO_CLIENT_ID: str
    YAHOO_CLIENT_SECRET: str
    YAHOO_CALLBACK_URL: str
    LINE_CLIENT_ID: str
    LINE_CLIENT_SECRET: str
    LINE_CALLBACK_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
