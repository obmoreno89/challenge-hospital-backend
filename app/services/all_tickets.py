from sqlmodel import Session, select
from sqlalchemy import func
import math
from typing import List
from app.schemas import TicketTable



def get_tickets(session: Session, page: int) -> List[TicketTable]:
    PAGE_SIZE = 10
    
    total_query = select(func.count()).select_from(TicketTable)
    total_register = session.exec(total_query).one()
    total_page = math.ceil(total_register / PAGE_SIZE)
    skip = (page - 1) * PAGE_SIZE
    statement = select(TicketTable).offset(skip).limit(PAGE_SIZE)
    
    games = session.exec(statement).all()
    
    return games, total_register, total_page