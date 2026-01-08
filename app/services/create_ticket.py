from sqlmodel import Session, select
from app.schemas import TicketTable, CreateTicket
from fastapi import Body, HTTPException, status
from app.utils import generate_uuid
from datetime import datetime

def post_ticket(session: Session, ticket_data: CreateTicket):
    folio = generate_uuid()
    
    extra_data = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estatus": 1
    }

    try:
        new_ticket = TicketTable.model_validate(ticket_data, update=extra_data)
        
        session.add(new_ticket)
        session.commit()
        session.refresh(new_ticket)
        return new_ticket
    except Exception as e:
        session.rollback()
        print(f"Error al insertar en DB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"folio": folio, "mensaje": "No se pudo guardar el ticket"}
        )