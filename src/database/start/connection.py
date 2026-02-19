from tortoise import Tortoise
from src.config import get_database_config
import logging

database_config = get_database_config()

async def start_connection():
  await Tortoise.init(
    db_url=f"postgresql://{database_config.DB_USER}:{database_config.DB_PASSWORD}@{database_config.DB_HOST}:{database_config.DB_PORT}/{database_config.DB_NAME}",
    modules={"models": ["src.models"]}
  )
  logging.info("✅ Conexión a la base de datos establecida correctamente")
  
  await Tortoise.generate_schemas()
  logging.info("✅ Esquemas de la base de datos generados correctamente")

async def stop_connection():
  await Tortoise.close_connections()
  logging.info("❌ Conexión a la base de datos cerrada correctamente")