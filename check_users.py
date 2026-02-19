"""
Script para verificar el estado de los usuarios en la base de datos.
Útil para diagnosticar problemas con hashes de passwords.

Uso: python check_users.py
"""
import asyncio
import logging
from tortoise import Tortoise
from src.config.tortoise import tortoise_config
from src.models import User
from src.lib.bycript import check_password

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


async def main():
    logger.info("Conectando a la base de datos...")
    await Tortoise.init(config=tortoise_config, _enable_global_fallback=True)
    
    try:
        users = await User.all()
        
        if not users:
            logger.warning("No hay usuarios en la base de datos")
            return
        
        logger.info(f"Encontrados {len(users)} usuario(s):")
        print()
        
        for user in users:
            print(f"Usuario: {user.username} ({user.email})")
            print(f"  ID: {user.id}")
            print(f"  Password (tipo): {type(user.password)}")
            print(f"  Password (longitud): {len(user.password) if user.password else 0}")
            print(f"  Password (primeros 20 chars): {str(user.password)[:20] if user.password else 'None'}...")
            
            # Intentar verificar con un password de prueba
            try:
                # Probar con "123456" (el password del seeder)
                is_valid = check_password("123456", user.password)
                print(f"  Hash válido para '123456': {'SÍ' if is_valid else 'NO'}")
            except Exception as e:
                print(f"  ERROR al verificar hash: {type(e).__name__}: {e}")
            
            print()
        
        logger.info("Diagnóstico completado")
        
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
