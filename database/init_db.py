import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.app.database import Base, engine, SessionLocal
from api.app.models.orm import HeroeDB

# Datos
HEROES_SEED = [
    {
        "nombre": "Olenthero",
        "descripcion": (
            "Nacido del fuego de la fragua y la dureza de las montañas, "
            "Olenthero es un titán que avanza lento pero imparable."
        ),
        "vida": 5.0, "mana": 1.0, "fisico": 8.0,
        "agilidad": 1.0,
    },
    {
        "nombre": "Thorgin",
        "descripcion": (
            "Tejedora de energías antiguas, Thorgin domina la magia "
            "primordial que brilla más allá del cielo nocturno."
        ),
        "vida": 1.0, "mana": 9.0, "fisico": 1.0,
        "agilidad": 4.0,
    },
    {
        "nombre": "Amalyria",
        "descripcion": (
            "Forjada en el espíritu de la Tierra Viva, Amalyria cura "
            "con la suavidad del musgo y protege con la fuerza de las raíces antiguas."
        ),
        "vida": 3.0, "mana": 7.0, "fisico": 2.0,
        "agilidad": 3.0,
    },
    {
        "nombre": "Basajörn",
        "descripcion": (
            "Hijo profundo del Bosque Eterno, Basajörn camina donde "
            "la luz apenas se atreve a entrar. Su arco jamás falla."
        ),
        "vida": 3.0, "mana": 2.0, "fisico": 5.0,
        "agilidad": 5.0,
    },
    {
        "nombre": "Lamyreth",
        "descripcion": (
            "Nacida de las cavernas donde la luz muere, Lamyreth se mueve "
            "como una sombra entre los árboles. Maestra del sigilo."
        ),
        "vida": 2.0, "mana": 3.0, "fisico": 3.0,
        "agilidad": 7.0,
    },
    {
        "nombre": "Sugarth",
        "descripcion": (
            "Forjado en el fuego celestial y marcado por el rayo, "
            "Sugarth es el juramento viviente de una orden olvidada."
        ),
        "vida": 4.0, "mana": 3.0, "fisico": 6.0,
        "agilidad": 2.0,
    },
]

def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas")

    db = SessionLocal()
    try:
        if db.query(HeroeDB).count() == 0:
            for data in HEROES_SEED:
                db.add(HeroeDB(**data))
            db.commit()
            print(f"{len(HEROES_SEED)} héroes insertados")
        else:
            print(f"Ya existen {db.query(HeroeDB).count()} héroes")
    finally:
        db.close()

    print("Base de datos de Euskayrim iniciada")


if __name__ == "__main__":
    init_database()
