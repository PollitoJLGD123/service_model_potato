from pydantic_settings import BaseSettings
from typing import Literal

class Config(BaseSettings):
  PORT: int
  DEBUG: bool
  DOMAIN: str
  ENV: Literal["development", "production"]
  NAME_COOKIE: str
  
  class Config: 
      env_file = ".env"
      extra = "ignore"
