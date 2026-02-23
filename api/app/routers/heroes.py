from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.services import database_service as db_svc

router = APIRouter(tags=["Heroes"])


@router.get("/heroes")
def get_heroes(db: Session = Depends(get_db)):
    """Endpoint para obtener la lista de héroes disponibles"""
    heroes = db_svc.get_heroes(db)
    return [
        {
            "id": h.id,
            "nombre": h.nombre,
            "descripcion": h.descripcion,
            "vida": h.vida,
            "mana": h.mana,
            "fisico": h.fisico,
            "agilidad": h.agilidad,
        }
        for h in heroes
    ]