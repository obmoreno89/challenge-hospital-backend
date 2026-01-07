from fastapi import APIRouter, Query, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlmodel import Session
from app.db import get_session
from app.schemas import ResponseTickets
from app.utils import generate_uuid
from app.services import get_tickets

router = APIRouter(tags=["Operaciones ticket"])

@router.get("/hospital/v1/operaciones/tickets", response_model=ResponseTickets)
def games(session: Session = Depends(get_session), page: int = Query(default=1)):
    
    folio = generate_uuid()
    
    if page <= 0:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "folio": folio,
                "mensaje": "no se admite la página 0",
            })
    
    tickets, total_reg, total_pag = get_tickets(session, page)

    if(page > total_pag and total_pag > 0):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return ResponseTickets(
        folio=folio,
        mensaje="Operación Exitosa",
        resultado=tickets,
        total_registros=total_reg,
        total_paginas=total_pag,
        pagina_actual=page
    )