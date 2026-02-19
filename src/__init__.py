from fastapi import FastAPI
from src.config import get_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.controllers import router
from tortoise.contrib.fastapi import register_tortoise
from src.config.tortoise import tortoise_config

config = get_config()

def create_app() -> FastAPI:
  app = FastAPI(
    title="API",
    version="1.0.0",
    debug=config.DEBUG,
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
  )
  
  # Usar config en lugar de db_url + modules (más limpio y consistente)
  register_tortoise(
    app, 
    config=tortoise_config,
    generate_schemas=True, 
    add_exception_handlers=True
  )
  
  app.add_middleware(GZipMiddleware,minimum_size=1024)

  app.include_router(router, prefix="/api/v1")
  
  return app