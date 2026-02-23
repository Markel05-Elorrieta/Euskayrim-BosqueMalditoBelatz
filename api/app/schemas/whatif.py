from pydantic import BaseModel


class WhatIf(BaseModel):

    olenthero_en_equipo: bool
    thorgin_en_equipo: bool   
    amalyria_en_equipo: bool
    basajorn_en_equipo: bool  
    lamyreth_en_equipo: bool 
    sugarth_en_equipo: bool   

    probabilidad_exito: float
    prediccion: str

    class Config:
        orm_mode = True

class WhatIfOut(WhatIf):
    id: int

