from pydantic import BaseModel

class IncursionHeroes(BaseModel):
    id_incursion: int
    id_heroe: int

    class Config:
        orm_mode = True
        
class IncursionHeroesOut(IncursionHeroes):
    id: int
