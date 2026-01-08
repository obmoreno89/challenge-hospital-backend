from pydantic import BaseModel, Field
from typing import Optional

class CreateTicket(BaseModel):
    asunto: str = Field(default=None, max_length=50)
    prioridad: int = Field(ge=1)
    detalle: str = Field(max_length=200)
    archivo_url: str
    
class UpdateTicket(BaseModel):
  asunto: Optional[str] = None
  prioridad: Optional[int] = None
  detalle: Optional[str] = None
  estatus: Optional[int] = None