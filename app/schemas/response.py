from typing import List 
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class Tickets(BaseModel):
    id: int = 3
    asunto: str = "fallas en software"
    prioridad: int = 1
    detalle: str = "el programa no sirve"
    fecha: str = "05052026"
    estatus: int = 1
    archivo_url: str = "http://"
    model_config = ConfigDict(from_attributes=True)
    

class ResponseTickets(BaseModel):
    folio: str = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    mensaje: str = "Operación exitosa"
    resultado: List[Tickets]
    total_registros: int = 20
    total_paginas: int = 2
    pagina_actual: int = 1
    
class ResponseDetailTicket(BaseModel):
    folio: str = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    mensaje: str = "Operación exitosa"
    resultado: List[Tickets]
    
class ResponseTicket(BaseModel):
    folio: str = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    mensaje: str = "Operación exitosa"