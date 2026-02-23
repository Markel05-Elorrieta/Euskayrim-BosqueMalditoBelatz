from pydantic import BaseModel
from typing import List


class Heroes(BaseModel):
    nombre: str
    descripcion: str
    vida : int
    mana : int
    fisico : int
    agilidad : int

    class Config:
        orm_mode = True

class HeroesOut(Heroes):
    id: int


