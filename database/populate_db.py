"""
Carga los datos del CSV de incursiones históricas en la base de datos.

Uso:
    python -m scripts.populate_db
    python -m scripts.populate_db --csv ad/data/bosque_maldito_belatz.csv
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# Asegurar que la raíz del proyecto esté en sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.init_db import init_database
from api.app.database import SessionLocal
from api.app.models.orm import IncursionDB, HeroeDB


# Columnas del CSV que se mapean a columnas de la tabla incursiones
INCURSION_COLUMNS = [
    "dificultad",
    "olenthero_en_equipo", "olenthero_vida", "olenthero_mana",
    "olenthero_fisico", "olenthero_agilidad",
    "thorgin_en_equipo", "thorgin_vida", "thorgin_mana",
    "thorgin_fisico", "thorgin_agilidad",
    "amalyria_en_equipo", "amalyria_vida", "amalyria_mana",
    "amalyria_fisico", "amalyria_agilidad",
    "basajorn_en_equipo", "basajorn_vida", "basajorn_mana",
    "basajorn_fisico", "basajorn_agilidad",
    "lamyreth_en_equipo", "lamyreth_vida", "lamyreth_mana",
    "lamyreth_fisico", "lamyreth_agilidad",
    "sugarth_en_equipo", "sugarth_vida", "sugarth_mana",
    "sugarth_fisico", "sugarth_agilidad",
    "exito",
]


# Mapa de nombre de héroe (clave en columnas CSV) → nombre en BD
HERO_NAMES = {
    "olenthero": "Olenthero",
    "thorgin": "Thorgin",
    "amalyria": "Amalyria",
    "basajorn": "Basajörn",
    "lamyreth": "Lamyreth",
    "sugarth": "Sugarth",
}


def populate_from_csv(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"No se encontró el archivo: {csv_path}")
        return

    print(f"Leyendo {csv_path.name} ...")
    df = pd.read_csv(csv_path)
    print(f"{len(df)} filas leídas")

    db = SessionLocal()
    try:
        # Cargar mapa de héroes desde la BD  {nombre_lower: HeroeDB}
        heroes_map: dict[str, HeroeDB] = {}
        for h in db.query(HeroeDB).all():
            heroes_map[h.nombre.lower().replace("ö", "o")] = h

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():
            # Construir diccionario de datos
            data: dict = {}
            for col in INCURSION_COLUMNS:
                val = row.get(col)
                if pd.isna(val):
                    data[col] = 0.0 if col != "exito" else None
                else:
                    try:
                        data[col] = float(val)
                    except (ValueError, TypeError):
                        data[col] = 0.0 if col != "exito" else None

            # Convertir campos _en_equipo a int
            for hero in HERO_NAMES:
                key = f"{hero}_en_equipo"
                if key in data and data[key] is not None:
                    data[key] = int(data[key])

            if data.get("exito") is not None:
                data["exito"] = int(data["exito"])

            incursion = IncursionDB(**data)

            # Poblar la relación N:M  incursion_heroes
            for hero_key, hero_nombre in HERO_NAMES.items():
                if data.get(f"{hero_key}_en_equipo") == 1:
                    hero_obj = heroes_map.get(hero_key)
                    if hero_obj:
                        incursion.heroes.append(hero_obj)

            db.add(incursion)
            inserted += 1

            # Commit por lotes para no saturar memoria
            if inserted % 500 == 0:
                db.commit()
                print(f"   ... {inserted} incursiones insertadas")

        db.commit()
        print(f"{inserted} incursiones insertadas ({skipped} filas saltadas)")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Puebla la BD de Euskayrim con datos del CSV")
    parser.add_argument(
        "--csv",
        type=str,
        default=str(ROOT / "ad" / "data" / "bosque_maldito_limpio.csv"),
        help="Ruta al archivo CSV de incursiones (por defecto el limpio)",
    )
    args = parser.parse_args()

    # Primero inicializar BD (crea tablas + siembra héroes)
    init_database()

    # Luego poblar con datos del CSV
    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path

    populate_from_csv(csv_path)

    # Resumen final
    db = SessionLocal()
    try:
        from api.app.models.orm import incursion_heroes
        from sqlalchemy import func
        print("\nResumen de la base de datos:")
        print(f"   Héroes:            {db.query(HeroeDB).count()}")
        print(f"   Incursiones:       {db.query(IncursionDB).count()}")
        ih_count = db.query(func.count()).select_from(incursion_heroes).scalar()
        print(f"   Incursion-Heroes:  {ih_count}")
        print("BASE DE DATOS LISTA")
    finally:
        db.close()


if __name__ == "__main__":
    main()
