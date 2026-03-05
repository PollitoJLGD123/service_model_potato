from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import Request

from src.models.prediccion import Prediccion
from src.models.surco import Surco

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


def build_fase2_placeholder() -> dict:
    # Keep DB-compatible non-null JSON until phase 2 is completed.
    return {
        "modelo": None,
        "clase_predicha": None,
        "confianza": None,
    }


def build_fase2_payload_placeholder() -> dict:
    # Placeholder structure that matches expected format for fase2_payload
    return {
        "resultados": {
            "efficient": {
                "clase_predicha": None,
                "confianza": None,
            }
        }
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
    surco_id: int | None = None,
) -> Prediccion:
    return await Prediccion.create(
        usuario_id=user_id,
        imagen_url=imagen_url,
        surco_id=surco_id,
        fase1_resumen=build_fase1_resumen(fase1_payload),
        fase1_payload=fase1_payload,
        fase2_resumen=build_fase2_placeholder(),
        fase2_payload=build_fase2_payload_placeholder(),
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
    # Find the most recent prediction for this user
    # that has fase1_payload but hasn't had fase2 classification results yet
    prediccion = await (
        Prediccion.filter(usuario_id=user_id, fase1_payload__isnull=False)
        .order_by("-id")
        .first()
    )
    if not prediccion:
        return None

    # Use placeholder if fase2_payload is None or empty
    if not fase2_payload:
        fase2_payload = build_fase2_payload_placeholder()

    prediccion.fase2_resumen = build_fase2_resumen(fase2_payload)
    prediccion.fase2_payload = fase2_payload
    await prediccion.save()
    return prediccion


async def list_all_surcos_for_user(user_id: int) -> list[dict]:
    """Get all surcos for a user across all their modules/lotes."""
    # Join: User -> Modulo -> Lote -> Surco
    surcos = await (
        Surco.all()
        .prefetch_related("lote", "lote__modulo", "lote__modulo__user")
        .filter(lote__modulo__user_id=user_id)
        .order_by("lote__modulo__id", "lote__id", "numero")
    )
    
    result = []
    for surco in surcos:
        await surco.fetch_related("lote")
        lote = surco.lote
        await lote.fetch_related("modulo")
        modulo = lote.modulo
        
        result.append({
            "id": surco.id,
            "numero": surco.numero,
            "descripcion": surco.descripcion,
            "lote_id": surco.lote_id,
            "lote_identificador": lote.identificador,
            "modulo_id": modulo.id,
            "modulo_nombre": modulo.nombre,
        })
    
    return result
