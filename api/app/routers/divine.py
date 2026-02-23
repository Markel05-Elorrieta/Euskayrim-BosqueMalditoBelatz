from itertools import combinations, product

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.schemas.incursion import Incursion
from api.app.services import database_service as db_svc
from api.app.services.prediction_service import predict_batch

router = APIRouter(tags=["Divine-Call"])

def _get_hero_keys() -> list[str]:
    return [
        field_name.replace("_en_equipo", "")
        for field_name in Incursion.model_fields
        if field_name.endswith("_en_equipo")
    ]
# Distribuciones candidatas de la Bendición de Ilargi (5 puntos por héroe):

# Distibuimos así para no sobrecargar el cálculo, ya que si se prueban todas las combis posibles,
# tardaría bastante en procesarse
_BLESSING_OPTIONS = [
    (5, 0, 0, 0),
    (0, 5, 0, 0),
    (0, 0, 5, 0),
    (0, 0, 0, 5),
]


class DivineCallRequest(BaseModel):
    dificultad: int = Field(ge=1, le=3, description="Dificultad de la incursión (1-3)")


class DivineCallResponse(BaseModel):
    heroes: list[str]
    probabilidad_maxima: float
    prediccion: str
    dificultad: int
    bendicion_optima: dict[str, dict[str, int]]
    todas_combinaciones: list[dict]


def _build_blessing_map(combo_names: list[str], blessings: tuple[tuple[int, int, int, int], ...]) -> dict[str, dict[str, int]]:
    blessing_map: dict[str, dict[str, int]] = {}
    for idx, hero_name in enumerate(combo_names):
        bv, bm, bf, ba = blessings[idx]
        blessing_map[hero_name] = {
            "vida": bv,
            "mana": bm,
            "fisico": bf,
            "agilidad": ba,
        }
    return blessing_map


@router.post("/divine-call", response_model=DivineCallResponse)
def divine_call(req: DivineCallRequest, db: Session = Depends(get_db)):
    """ Endpoint que recibe la dificultad de la incursión y devuelve la mejor combinación de héroes para maximizar la probabilidad de éxito,
    junto con la predicción y la probabilidad.
    También devuelve todas las combinaciones ordenadas por probabilidad"""
    heroes_db = db_svc.get_heroes(db)
    hero_map = {}
    for h in heroes_db:
        key = h.nombre.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        hero_map[key] = {
            "nombre": h.nombre,
            "vida": h.vida,
            "mana": h.mana,
            "fisico": h.fisico,
            "agilidad": h.agilidad,
        }

    hero_keys = _get_hero_keys()

    # Generar todas las combinaciones de 4 héroes entre los disponibles
    available_keys = [k for k in hero_keys if k in hero_map]
    combos = list(combinations(available_keys, 4))

    # Construir todos los Incursion objects de una vez para hacer batch predict
    all_incursions: list[Incursion] = []
    # Metadatos para reconstruir resultados después
    meta: list[tuple[int, list[str], tuple[tuple[int, int, int, int], ...]]] = []

    for combo_idx, combo in enumerate(combos):
        combo_names = [hero_map[k]["nombre"] for k in combo]
        for blessings in product(_BLESSING_OPTIONS, repeat=4):
            data = {"dificultad": float(req.dificultad)}
            blessing_idx = 0
            for key in hero_keys:
                if key in combo:
                    hero = hero_map[key]
                    bv, bm, bf, ba = blessings[blessing_idx]
                    blessing_idx += 1
                    data[f"{key}_en_equipo"] = 1
                    data[f"{key}_vida"] = hero["vida"] + bv
                    data[f"{key}_mana"] = hero["mana"] + bm
                    data[f"{key}_fisico"] = hero["fisico"] + bf
                    data[f"{key}_agilidad"] = hero["agilidad"] + ba
                else:
                    data[f"{key}_en_equipo"] = 0
                    data[f"{key}_vida"] = 0.0
                    data[f"{key}_mana"] = 0.0
                    data[f"{key}_fisico"] = 0.0
                    data[f"{key}_agilidad"] = 0.0
            all_incursions.append(Incursion(**data))
            meta.append((combo_idx, combo_names, blessings))

    # Una sola llamada al modelo para todas las filas
    batch_results = predict_batch(all_incursions)

    # Agregar por combinación: quedarse con la mejor distribución de bendición
    combo_best: dict[int, dict] = {}
    for i, result in enumerate(batch_results):
        combo_idx, combo_names, blessings = meta[i]
        if combo_idx not in combo_best or result["probabilidad_exito"] > combo_best[combo_idx]["probabilidad_exito"]:
            combo_best[combo_idx] = {
                "heroes": combo_names,
                "probabilidad_exito": result["probabilidad_exito"],
                "prediccion": result["prediccion"],
                "bendicion": _build_blessing_map(combo_names, blessings),
            }

    all_results = list(combo_best.values())
    all_results.sort(key=lambda x: x["probabilidad_exito"], reverse=True)

    best = all_results[0]
    best_combo = best["heroes"]
    best_prob = best["probabilidad_exito"]
    best_pred = best["prediccion"]
    best_blessing = best["bendicion"]

    return DivineCallResponse(
        heroes=best_combo,
        probabilidad_maxima=best_prob,
        prediccion=best_pred,
        dificultad=req.dificultad,
        bendicion_optima=best_blessing,
        todas_combinaciones=all_results,
    )
