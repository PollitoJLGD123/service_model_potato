from tortoise import Tortoise
import logging
from src.config.tortoise import tortoise_config

logger = logging.getLogger("LOGGER_DATABASE")

async def start_connection():
  await Tortoise.init(config=tortoise_config)
  logger.info("Conexion a la base de datos establecida correctamente")
  try:
    await Tortoise.generate_schemas(safe=True)
    logger.info("Esquemas de la base de datos generados correctamente")
  except Exception as e:
    logger.error(f"Error al generar los esquemas de la base de datos: {e}")
    raise e

async def stop_connection():
  await Tortoise.close_connections()
  logger.info("Conexion a la base de datos cerrada correctamente")