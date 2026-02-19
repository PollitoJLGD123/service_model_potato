from tortoise import Tortoise
import logging
from src.config.tortoise import tortoise_config

logger = logging.getLogger(__name__)

async def start_connection():
  await Tortoise.init(config=tortoise_config)
  logging.info("✅ Conexión a la base de datos establecida correctamente")
  
  # await Tortoise.generate_schemas()
  # logging.info("✅ Esquemas de la base de datos generados correctamente")

async def stop_connection():
  await Tortoise.close_connections()
  logging.info("❌ Conexión a la base de datos cerrada correctamente")