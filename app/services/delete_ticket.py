from sqlmodel import Session
from app.schemas import TicketTable


from sqlmodel import Session, select
from app.schemas import TicketTable

def delete_ticket_by_id(session: Session, ticket_id: int) -> bool:
    statement = select(TicketTable).where(TicketTable.id == ticket_id)
    result = session.exec(statement)
    ticket = result.first()

    if not ticket:
        return False

    try:
        session.delete(ticket)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar: {e}")
        return False