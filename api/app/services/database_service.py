from typing import List, Optional

from sqlalchemy.orm import Session

from api.app.models.orm import HeroeDB, IncursionDB, PrediccionDB


# ======================== HÉROES ========================


def get_heroes(db: Session) -> List[HeroeDB]:
    """Devuelve todos los héroes"""
    return db.query(HeroeDB).order_by(HeroeDB.id).all()


def get_heroe_by_nombre(db: Session, nombre: str) -> Optional[HeroeDB]:
    """Busca un héroe por nombre"""
    return db.query(HeroeDB).filter(HeroeDB.nombre.ilike(nombre)).first()


def get_heroe_by_id(db: Session, heroe_id: int) -> Optional[HeroeDB]:
    """Busca un héroe por ID"""
    return db.query(HeroeDB).get(heroe_id)


def create_heroe(db: Session, **kwargs) -> HeroeDB:
    """Crea un héroe nuevo"""
    heroe = HeroeDB(**kwargs)
    db.add(heroe)
    db.commit()
    db.refresh(heroe)
    return heroe

# ======================== INCURSIONES ========================


def get_incursiones(
    db: Session, skip: int = 0, limit: int = 100
) -> List[IncursionDB]:
    """Devuelve incursiones con paginación"""
    return (
        db.query(IncursionDB)
        .order_by(IncursionDB.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_incursion_by_id(db: Session, incursion_id: int) -> Optional[IncursionDB]:
    """Busca una incursión por ID"""
    return db.query(IncursionDB).get(incursion_id)


def count_incursiones(db: Session) -> int:
    """Devuelve el conteo total de incursiones"""
    return db.query(IncursionDB).count()


def create_incursion(db: Session, **kwargs) -> IncursionDB:
    """Crea un registro de incursión"""
    incursion = IncursionDB(**kwargs)
    db.add(incursion)
    db.commit()
    db.refresh(incursion)
    return incursion


def bulk_create_incursiones(db: Session, incursiones: list[dict]) -> int:
    """Inserta múltiples incursiones de golpe. Devuelve la cantidad insertada"""
    objects = [IncursionDB(**data) for data in incursiones]
    db.bulk_save_objects(objects)
    db.commit()
    return len(objects)


# ======================== PREDICCIONES ========================


def get_predicciones(
    db: Session, skip: int = 0, limit: int = 50
) -> List[PrediccionDB]:
    """Devuelve predicciones con paginación"""
    return (
        db.query(PrediccionDB)
        .order_by(PrediccionDB.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_prediccion(db: Session, **kwargs) -> PrediccionDB:
    """Registra una predicción What-If en BD"""
    pred = PrediccionDB(**kwargs)
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


def count_predicciones(db: Session) -> int:
    """Devuelve el conteo total de predicciones"""
    return db.query(PrediccionDB).count()
