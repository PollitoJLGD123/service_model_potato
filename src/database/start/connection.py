from tortoise import Tortoise
import logging
from src.config.tortoise import tortoise_config

logger = logging.getLogger("LOGGER_DATABASE")

async def start_connection():
  # _enable_global_fallback=True hace que las peticiones (otras tareas) vean el contexto
  # de Tortoise; si no, solo el lifespan tendría contexto y daría RuntimeError en los endpoints.
  await Tortoise.init(config=tortoise_config, _enable_global_fallback=True)
  logger.info("Conexion a la base de datos establecida correctamente")
  try:
    await Tortoise.generate_schemas(safe=True)
    logger.info("Esquemas de la base de datos generados correctamente")
  except Exception as e:
    logger.error("Error al generar los esquemas de la base de datos: %s", e)
    raise

async def stop_connection():
  await Tortoise.close_connections()
  logger.info("Conexion a la base de datos cerrada correctamente")