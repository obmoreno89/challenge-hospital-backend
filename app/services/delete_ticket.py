from sqlmodel import Session
from app.schemas import TicketTable


def delete_ticket_by_id(session: Session, ticket_id: int) -> bool:
    statement = session.query(TicketTable).where(TicketTable.id == ticket_id)
    ticket = session.exec(statement).first()
    
    if not ticket:
        return False
    
    session.delete(ticket)
    session.commit()
    return True