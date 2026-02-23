from api.app.models.domain import (
    Heroe,
    Olenthero,
    Thorgin,
    Amalyria,
    Basajorn,
    Lamyreth,
    Sugarth,
    BendicionIlargi,
    Equipo,
    Incursion,
)

class TestHeroe:
    def test_crear_heroe(self):
        h = Heroe("TestHero", vida=100, mana=50, fisico=80, agilidad=60)
        assert h.nombre == "TestHero"
        assert h.vida == 100
        assert h.mana == 50
        assert h.fisico == 80
        assert h.agilidad == 60

    def test_mostrar_info(self):
        h = Heroe("TestHero", vida=10, mana=20, fisico=30, agilidad=40)
        info = h.mostrar_info()
        assert "TestHero" in info
        assert "10" in info
        assert "20" in info
        

class TestSubclasesHeroe:
    def test_olenthero(self):
        h = Olenthero(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Olenthero"

    def test_thorgin(self):
        h = Thorgin(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Thorgin"

    def test_amalyria(self):
        h = Amalyria(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Amalyria"

    def test_basajorn(self):
        h = Basajorn(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Basajörn"

    def test_lamyreth(self):
        h = Lamyreth(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Lamyreth"

    def test_sugarth(self):
        h = Sugarth(vida=1, mana=2, fisico=3, agilidad=4)
        assert h.nombre == "Sugarth"



class TestBendicionIlargi:
    def test_total_puntos(self):
        b = BendicionIlargi(vida=1, mana=1, fisico=2, agilidad=1)
        assert b.total_puntos() == 5

    def test_es_valida_correcto(self):
        b = BendicionIlargi(vida=2, mana=1, fisico=1, agilidad=1)
        assert b.es_valida() is True

    def test_es_valida_incorrecto(self):
        b = BendicionIlargi(vida=10, mana=10, fisico=10, agilidad=10)
        assert b.es_valida() is False

    def test_default_cero(self):
        b = BendicionIlargi()
        assert b.total_puntos() == 0
        assert b.es_valida() is False



class TestEquipo:
    def _hacer_equipo(self, n_heroes=4, bendicion_total=5):
        heroes_cls = [Olenthero, Thorgin, Amalyria, Basajorn, Lamyreth, Sugarth]
        heroes = [
            cls(vida=50, mana=50, fisico=50, agilidad=50)
            for cls in heroes_cls[:n_heroes]
        ]
        bendicion = BendicionIlargi(vida=bendicion_total, mana=0, fisico=0, agilidad=0)
        return Equipo(heroes, bendicion)

    def test_equipo_valido(self):
        eq = self._hacer_equipo(4, 5)
        assert eq.es_valido() is True

    def test_equipo_invalido_pocos_heroes(self):
        eq = self._hacer_equipo(3, 5)
        assert eq.es_valido() is False

    def test_equipo_invalido_muchos_heroes(self):
        eq = self._hacer_equipo(5, 5)
        assert eq.es_valido() is False

    def test_equipo_invalido_bendicion(self):
        eq = self._hacer_equipo(4, 10)
        assert eq.es_valido() is False

    def test_equipo_heroes_duplicados(self):
        h = Olenthero(vida=1, mana=1, fisico=1, agilidad=1)
        bendicion = BendicionIlargi(vida=5)
        eq = Equipo([h, h, h, h], bendicion)
        assert eq.es_valido() is False

    def test_mostrar_equipo(self):
        eq = self._hacer_equipo(4, 5)
        texto = eq.mostrar_equipo()
        assert "Equipo" in texto
        assert "Olenthero" in texto


class TestIncursionDomain:
    def test_incursion_exito(self):
        eq = TestEquipo()._hacer_equipo()
        inc = Incursion(eq, exito=True)
        assert inc.exito is True
        assert "ÉXITO" in inc.mostrar_resultado()

    def test_incursion_fracaso(self):
        eq = TestEquipo()._hacer_equipo()
        inc = Incursion(eq, exito=False)
        assert inc.exito is False
        assert "FRACASO" in inc.mostrar_resultado()
