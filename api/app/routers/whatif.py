from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.schemas.incursion import Incursion
from api.app.services import database_service as db_svc
from api.app.services.prediction_service import predict

router = APIRouter(tags=["What-If"])


@router.post("/what-if")
def predict_success(incursion: Incursion, db: Session = Depends(get_db)):
    """Endpoint que recibe los datos de una incursión (dificultad y héroes) y devuelve la predicción de éxito junto con la probabilidad"""
    result = predict(incursion)

    # Guardar la predicción en BD
    db_svc.create_prediccion(
        db,
        dificultad=incursion.dificultad,
        olenthero_en_equipo=incursion.olenthero_en_equipo,
        thorgin_en_equipo=incursion.thorgin_en_equipo,
        amalyria_en_equipo=incursion.amalyria_en_equipo,
        basajorn_en_equipo=incursion.basajorn_en_equipo,
        lamyreth_en_equipo=incursion.lamyreth_en_equipo,
        sugarth_en_equipo=incursion.sugarth_en_equipo,
        probabilidad_exito=result["probabilidad_exito"],
        prediccion=result["prediccion"],
    )

    return result
