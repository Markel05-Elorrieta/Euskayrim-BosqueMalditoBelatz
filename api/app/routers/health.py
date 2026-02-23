from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.ml.model_loader import ModelLoader
from api.app.services import database_service as db_svc

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Endpoint de salud para verificar que la API y el modelo están funcionando correctamente"""
    return {
        "status": "ok",
        "modelo_cargado": ModelLoader.is_loaded(),
        "incursiones_en_bd": db_svc.count_incursiones(db),
        "predicciones_realizadas": db_svc.count_predicciones(db),
    }
