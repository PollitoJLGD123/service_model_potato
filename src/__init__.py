from fastapi import FastAPI
from src.config import get_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.controllers import router
from src.tasks.tasks import lifespan

config = get_config()

def create_app() -> FastAPI:
  app = FastAPI(
    title="API",
    version="1.0.0",
    debug=config.DEBUG,
    lifespan=lifespan,
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
  
  app.add_middleware(GZipMiddleware,minimum_size=1024)

  app.include_router(router, prefix="/api/v1")
  
  return app