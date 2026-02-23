from unittest.mock import patch, MagicMock

from api.app.models.orm import HeroeDB


# ======================== GET / ========================


class TestHome:
    def test_home(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "mensaje" in data
        assert "Bienvenido" in data["mensaje"]


# ======================== GET /health ========================


class TestHealth:
    def test_health_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "modelo_cargado" in data
        assert "incursiones_en_bd" in data
        assert "predicciones_realizadas" in data


# ======================== GET /heroes ========================


class TestHeroes:
    def test_heroes_vacio(self, client):
        """Sin datos en la BD, devuelve lista vacía"""
        resp = client.get("/heroes")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_heroes_con_datos(self, client, db_session):
        """Insertamos un héroe y verificamos que aparece"""
        heroe = HeroeDB(
            nombre="Olenthero",
            descripcion="Mago antiguo",
            vida=80.0,
            mana=60.0,
            fisico=50.0,
            agilidad=40.0,
        )
        db_session.add(heroe)
        db_session.commit()

        resp = client.get("/heroes")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["nombre"] == "Olenthero"
        assert data[0]["vida"] == 80.0


# ======================== POST /what-if ========================


class TestWhatIf:
    @patch("api.app.routers.whatif.predict")
    def test_what_if_exitoso(self, mock_predict, client, sample_incursion_payload):
        """Mockeamos la predicción para no depender del modelo ML"""
        mock_predict.return_value = {
            "probabilidad_exito": 0.85,
            "prediccion": "Victoria",
            "dificultad_incursion": 5.0,
        }
        resp = client.post("/what-if", json=sample_incursion_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["prediccion"] == "Victoria"
        assert data["probabilidad_exito"] == 0.85
        mock_predict.assert_called_once()

    def test_what_if_payload_invalido(self, client):
        """Enviar un body vacío debe dar 422"""
        resp = client.post("/what-if", json={})
        assert resp.status_code == 422

    def test_what_if_sin_body(self, client):
        """Sin body debe dar 422"""
        resp = client.post("/what-if")
        assert resp.status_code == 422