from typing import Optional
from sqlmodel import Field, SQLModel

class TicketBase(SQLModel):
    asunto: str = Field(max_length=50)
    prioridad: int = Field(ge=1)
    detalle: str = Field(max_length=200)
    fecha: str
    estatus: int = Field(ge=1)
    archivo_url: str


class TicketTable(TicketBase, table=True):
    __tablename__ = "reportes"
    
    id: Optional[int] = Field(default=None, primary_key=True)