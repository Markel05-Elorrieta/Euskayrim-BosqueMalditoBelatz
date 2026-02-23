from pydantic import BaseModel


class Incursion(BaseModel):

    dificultad: float

    # Olenthero
    olenthero_en_equipo: int
    olenthero_vida: float
    olenthero_mana: float
    olenthero_fisico: float
    olenthero_agilidad: float

    # Thorgin
    thorgin_en_equipo: int
    thorgin_vida: float
    thorgin_mana: float
    thorgin_fisico: float
    thorgin_agilidad: float

    # Amalyria
    amalyria_en_equipo: int
    amalyria_vida: float
    amalyria_mana: float
    amalyria_fisico: float
    amalyria_agilidad: float

    # Basajorn
    basajorn_en_equipo: int
    basajorn_vida: float
    basajorn_mana: float
    basajorn_fisico: float
    basajorn_agilidad: float

    # Lamyreth
    lamyreth_en_equipo: int
    lamyreth_vida: float
    lamyreth_mana: float
    lamyreth_fisico: float
    lamyreth_agilidad: float

    # Sugarth
    sugarth_en_equipo: int
    sugarth_vida: float
    sugarth_mana: float
    sugarth_fisico: float
    sugarth_agilidad: float

    class Config:
        orm_mode = True
        
class IncursionOut(Incursion):
    id: int
