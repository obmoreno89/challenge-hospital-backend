from sqlmodel import Session, select
from app.schemas import TicketTable, UpdateTicket
from fastapi import Body



def patch_ticket(session:Session, ticket_id: int, ticket_data: UpdateTicket = Body()):
    statement = select(TicketTable).where(TicketTable.id == ticket_id)
    ticket = session.exec(statement).first()
    
    if not ticket:
        return None
    
    update_data = ticket_data.model_dump(exclude_unset=True)
    ticket.sqlmodel_update(update_data)
        
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    return ticket