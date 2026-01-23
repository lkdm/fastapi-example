from pydantic_settings import BaseSettings

class Configuration(BaseSettings):
	API_V1_STR: str = "/api/v1"
