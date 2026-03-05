from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import Request

from src.models.prediccion import Prediccion

PREDICTIONS_DIR = Path(__file__).parent.parent.parent / "public" / "predictions"

_CONTENT_TYPE_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _iso(value) -> str | None:
    return value.isoformat() if value else None


def save_image_locally(img_bytes: bytes, content_type: str | None, request: Request) -> str:
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    ext = _CONTENT_TYPE_EXT.get(content_type or "", ".jpg")
    filename = f"{uuid.uuid4().hex}{ext}"
    (PREDICTIONS_DIR / filename).write_bytes(img_bytes)

    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/public/predictions/{filename}"


def build_fase1_resumen(fase1_payload: dict) -> dict:
    predictions = fase1_payload.get("predictions", []) or []
    clases = sorted({p.get("class", "") for p in predictions if p.get("class")})
    return {
        "has_matches": bool(fase1_payload.get("has_matches", False)),
        "total_detecciones": len(predictions),
        "clases_detectadas": clases,
    }


def build_fase2_resumen(full_payload: dict) -> dict:
    efficient = full_payload.get("resultados", {}).get("efficient", {})
    return {
        "modelo": "efficient",
        "clase_predicha": efficient.get("clase_predicha"),
        "confianza": efficient.get("confianza"),
    }


def prediccion_to_dict(p: Prediccion) -> dict:
    return {
        "id": p.id,
        "surco_id": p.surco_id,
        "usuario_id": p.usuario_id,
        "imagen_url": p.imagen_url,
        "fase1_resumen": p.fase1_resumen,
        "fase1_payload": p.fase1_payload,
        "fase2_resumen": p.fase2_resumen,
        "fase2_payload": p.fase2_payload,
        "fecha": _iso(p.fecha),
        "created_at": _iso(p.created_at),
        "updated_at": _iso(p.updated_at),
    }


async def create_prediccion_fase1(
    user_id: int,
    imagen_url: str,
    fase1_payload: dict,
) -> Prediccion:
    return await Prediccion.create(
        usuario_id=user_id,
        imagen_url=imagen_url,
        fase1_resumen=build_fase1_resumen(fase1_payload),
        fase1_payload=fase1_payload,
    )


async def list_predicciones_by_user(user_id: int) -> list[dict]:
    predicciones = await (
        Prediccion.filter(usuario_id=user_id)
        .order_by("-id")
        .all()
    )
    return [prediccion_to_dict(p) for p in predicciones]


async def update_prediccion_fase2(
    user_id: int,
    fase2_payload: dict,
) -> Prediccion | None:
    prediccion = await (
        Prediccion.filter(usuario_id=user_id, fase2_payload__isnull=True)
        .order_by("-id")
        .first()
    )
    if not prediccion:
        return None

    prediccion.fase2_resumen = build_fase2_resumen(fase2_payload)
    prediccion.fase2_payload = fase2_payload
    await prediccion.save()
    return prediccion
