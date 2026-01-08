from fastapi import APIRouter, Query, status, Depends, Path, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlmodel import Session
from app.db import get_session
from app.schemas import ResponseTickets, ResponseDetailTicket, UpdateTicket, ResponseTicket, CreateTicket
from app.utils import generate_uuid
from app.services import get_tickets, get_detail_ticket, patch_ticket, delete_ticket_by_id, post_ticket

router = APIRouter(tags=["Operaciones ticket"])

@router.get("/hospital/v1/operaciones/tickets", response_model=ResponseTickets)
def tickets(session: Session = Depends(get_session), page: int = Query(default=1)):
    
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

@router.get("/hospital/v1/operaciones/tickets/{ticket_id}", response_model=ResponseDetailTicket,)
def detail_ticket(session: Session = Depends(get_session), ticket_id: int = Path()):
    folio = generate_uuid()
    ticket =  get_detail_ticket(session, ticket_id)
    
    if ticket is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return ResponseDetailTicket(
        folio=folio,
        mensaje="Operación Exitosa",
        resultado=ticket
    )
    
@router.patch("/hospital/v1/operaciones/actualiza/{ticket_id}", response_model=ResponseTicket,)
def parcial_update(session: Session = Depends(get_session), ticket_id: int = Path(), ticket_data: UpdateTicket = Body()):
    folio = generate_uuid()
    update_tickets = patch_ticket(session, ticket_id, ticket_data)
    
    if update_tickets is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    if ticket_data.stock is not None:
        if ticket_data.stock == 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "folio": folio,
            "mensaje": "no puedes mandar un stock en 0"
        }) 
        if ticket_data.stock < 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "folio": folio,
            "mensaje": "no se permite numeros en negativo"
            })      
    
    return ResponseTicket(
        folio=folio,
        mensaje="Operación exitosa",
    )
    
@router.delete("/hospital/v1/operaciones/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
def delete_ticket(ticket_id: int = Path(), session: Session = Depends(get_session)):
    folio = generate_uuid()
    
    success = delete_ticket_by_id(session, ticket_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail={"folio": folio, 
                    "mensaje": "El ticket no existe"
            }
        )
    
    return ResponseTicket(
        folio=folio,
        mensaje="Operación exitosa",
    )
    
@router.post("/hospital/v1/operaciones/crear", response_model=ResponseTicket)
def create_ticket(session: Session = Depends(get_session), ticket_data: CreateTicket = Body()):
    folio = generate_uuid()
    new_ticket = post_ticket(session, ticket_data)
    
    return ResponseTicket(
        folio= folio,
        mensaje= "Operación exitosa"
    )