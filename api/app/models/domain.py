class Heroe:
    def __init__(self, nombre, vida, mana, fisico, agilidad):
        self.nombre = nombre
        self.vida = vida
        self.mana = mana
        self.fisico = fisico
        self.agilidad = agilidad
    
    def mostrar_info(self):
        return f"{self.nombre} - Vida: {self.vida}, Mana: {self.mana}, Físico: {self.fisico}, Agilidad: {self.agilidad}"


class Olenthero(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Olenthero", vida, mana, fisico, agilidad)


class Thorgin(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Thorgin", vida, mana, fisico, agilidad)


class Amalyria(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Amalyria", vida, mana, fisico, agilidad)


class Basajorn(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Basajörn", vida, mana, fisico, agilidad)


class Lamyreth(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Lamyreth", vida, mana, fisico, agilidad)


class Sugarth(Heroe):
    def __init__(self, vida, mana, fisico, agilidad):
        super().__init__("Sugarth", vida, mana, fisico, agilidad)


class BendicionIlargi:
    def __init__(self, vida=0, mana=0, fisico=0, agilidad=0):
        self.vida = vida
        self.mana = mana
        self.fisico = fisico
        self.agilidad = agilidad
    
    def total_puntos(self):
        return self.vida + self.mana + self.fisico + self.agilidad
    
    def es_valida(self):
        return self.total_puntos() == 5


class Equipo:
    def __init__(self, heroes, bendicion):
        self.heroes = heroes
        self.bendicion = bendicion
    
    def es_valido(self):
        if len(self.heroes) != 4:
            return False

        nombres = [heroe.nombre for heroe in self.heroes]
        if len(nombres) != len(set(nombres)):
            return False

        return self.bendicion.es_valida()
    
    def mostrar_equipo(self):
        resultado = "Equipo:\n"
        for heroe in self.heroes:
            resultado += f"  - {heroe.mostrar_info()}\n"
        resultado += f"Bendición de Ilargi: +{self.bendicion.total_puntos()} puntos distribuidos\n"
        return resultado

class Incursion:
    def __init__(self, equipo, exito):
        self.equipo = equipo
        self.exito = exito
    
    def mostrar_resultado(self):
        resultado = "Incursión\n"
        resultado += self.equipo.mostrar_equipo()
        resultado += f"Resultado: {'ÉXITO' if self.exito else 'FRACASO'}"
        return resultado