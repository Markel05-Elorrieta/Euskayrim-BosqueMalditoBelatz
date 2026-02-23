from api.app.models.orm import HeroeDB, IncursionDB, PrediccionDB
from api.app.services import database_service as db_svc


# ======================== Héroes ========================


class TestHeroesService:
    def test_get_heroes_vacio(self, db_session):
        result = db_svc.get_heroes(db_session)
        assert result == []

    def test_create_heroe(self, db_session):
        h = db_svc.create_heroe(
            db_session,
            nombre="Olenthero",
            descripcion="Mago antiguo",
            vida=80.0,
            mana=60.0,
            fisico=50.0,
            agilidad=40.0,
        )
        assert h.id is not None
        assert h.nombre == "Olenthero"

    def test_get_heroe_by_nombre(self, db_session):
        db_svc.create_heroe(db_session, nombre="Thorgin", vida=90, mana=30, fisico=85, agilidad=35)
        found = db_svc.get_heroe_by_nombre(db_session, "thorgin")
        assert found is not None
        assert found.nombre == "Thorgin"

    def test_get_heroe_by_nombre_no_existe(self, db_session):
        assert db_svc.get_heroe_by_nombre(db_session, "NoExiste") is None

    def test_get_heroe_by_id(self, db_session):
        h = db_svc.create_heroe(db_session, nombre="Amalyria", vida=50, mana=95, fisico=20, agilidad=60)
        found = db_svc.get_heroe_by_id(db_session, h.id)
        assert found is not None
        assert found.nombre == "Amalyria"


# ======================== Incursiones ========================


class TestIncursionesService:
    def test_count_incursiones_vacio(self, db_session):
        assert db_svc.count_incursiones(db_session) == 0

    def test_create_incursion(self, db_session):
        inc = db_svc.create_incursion(db_session, dificultad=5.0, exito=1)
        assert inc.id is not None
        assert inc.dificultad == 5.0

    def test_count_incursiones(self, db_session):
        db_svc.create_incursion(db_session, dificultad=3.0, exito=1)
        db_svc.create_incursion(db_session, dificultad=7.0, exito=0)
        assert db_svc.count_incursiones(db_session) == 2

    def test_get_incursiones_paginacion(self, db_session):
        for i in range(5):
            db_svc.create_incursion(db_session, dificultad=float(i), exito=1)
        result = db_svc.get_incursiones(db_session, skip=0, limit=3)
        assert len(result) == 3

    def test_bulk_create_incursiones(self, db_session):
        datos = [
            {"dificultad": 1.0, "exito": 1},
            {"dificultad": 2.0, "exito": 0},
            {"dificultad": 3.0, "exito": 1},
        ]
        count = db_svc.bulk_create_incursiones(db_session, datos)
        assert count == 3
        assert db_svc.count_incursiones(db_session) == 3


# ======================== Predicciones ========================


class TestPrediccionesService:
    def test_count_predicciones_vacio(self, db_session):
        assert db_svc.count_predicciones(db_session) == 0

    def test_create_prediccion(self, db_session):
        pred = db_svc.create_prediccion(
            db_session,
            dificultad=5.0,
            olenthero_en_equipo=1,
            thorgin_en_equipo=1,
            amalyria_en_equipo=1,
            basajorn_en_equipo=1,
            lamyreth_en_equipo=0,
            sugarth_en_equipo=0,
            probabilidad_exito=0.85,
            prediccion="Victoria",
        )
        assert pred.id is not None
        assert pred.prediccion == "Victoria"

    def test_count_predicciones_con_datos(self, db_session):
        db_svc.create_prediccion(
            db_session,
            dificultad=5.0,
            probabilidad_exito=0.75,
            prediccion="Victoria",
        )
        db_svc.create_prediccion(
            db_session,
            dificultad=8.0,
            probabilidad_exito=0.3,
            prediccion="Derrota",
        )
        assert db_svc.count_predicciones(db_session) == 2
