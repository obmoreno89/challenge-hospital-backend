from sqlmodel import Session, select
from app.schemas import TicketTable, UpdateTicket
from fastapi import Body



def patch_ticket(session:Session, ticket_id: int, ticket_data: UpdateTicket = Body()):
    statement = select(TicketTable).where(TicketTable.id == ticket_id)
    ticket = session.exec(statement).first()
    there_stock: bool = True
    
    if not ticket:
        return None, False
    
    update_data = ticket_data.model_dump(exclude_unset=True, exclude={"stock", "isIncrease"})
    ticket.sqlmodel_update(update_data)
        
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    return ticket, there_stock