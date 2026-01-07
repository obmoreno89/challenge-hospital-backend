from pydantic import BaseModel, Field

class CreateTicket(BaseModel):
    asunto: str = Field(default=None, max_length=50)
    prioridad: int = Field(ge=1)
    detalle: str = Field(max_length=200)
    archivo_url: str
    
class UpdateTicket():
    estatus: int = Field(ge=1)