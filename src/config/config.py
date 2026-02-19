from pydantic_settings import BaseSettings

class Config(BaseSettings):
  PORT: int
  DEBUG: bool
  
  class Config: 
      env_file = ".env"
      extra = "ignore"
