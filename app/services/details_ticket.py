from sqlmodel import Session, select
from typing import List, Optional
from app.schemas import TicketTable

def get_detail_ticket(session: Session, ticket_id: int) -> Optional[TicketTable]:
    statement = select(TicketTable).where(TicketTable.id == ticket_id)
    ticket = session.exec(statement).first()
    return ticket
