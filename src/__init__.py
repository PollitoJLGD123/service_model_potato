import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from src.config import get_config
from src.config.tortoise import tortoise_config
from src.controllers import router
from src.middleware.auth import JWTAuthMiddleware


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

config = get_config()


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000",
    )

    return [
        origin.strip().rstrip("/")
        for origin in raw_origins.split(",")
        if origin.strip()
    ]


def get_env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def create_app() -> FastAPI:
    app = FastAPI(
        title="API",
        version="1.0.0",
        debug=config.DEBUG,
    )

    # Primero se agrega autenticación.
    app.add_middleware(JWTAuthMiddleware)

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1024,
    )

    # Se agrega CORS al final para que sea el middleware más externo
    # y atienda las solicitudes OPTIONS antes que la autenticación.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
            "PATCH",
        ],
        allow_headers=[
            "Accept",
            "Authorization",
            "Content-Type",
            "Origin",
            "X-Requested-With",
        ],
        expose_headers=[],
        max_age=60 * 60 * 24,
    )

    register_tortoise(
        app,
        config=tortoise_config,
        generate_schemas=get_env_bool(
            "GENERATE_SCHEMAS",
            default=False,
        ),
        add_exception_handlers=True,
    )

    app.include_router(
        router,
        prefix="/api/v1",
    )

    public_dir = Path(__file__).parent.parent / "public"
    public_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    app.mount(
        "/public",
        StaticFiles(directory=str(public_dir)),
        name="public",
    )

    return app