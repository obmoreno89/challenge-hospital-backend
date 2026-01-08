from sqlmodel import Session, select
from app.schemas import TicketTable, UpdateTicket
from fastapi import Body



def patch_ticket(session:Session, ticket_id: int, ticket_data: UpdateTicket = Body()):
    statement = select(TicketTable).where(TicketTable.id == ticket_id)
    game = session.exec(statement).first()
    there_stock: bool = True
    
    if not game:
        return None, False
    
    update_data = ticket_data.model_dump(exclude_unset=True, exclude={"stock", "isIncrease"})
    game.sqlmodel_update(update_data)
    
    if ticket_data.stock is not None:
        if not ticket_data.isIncrease:
            if ticket_data.stock > game.stock:
                there_stock = False
                return game, there_stock
            game.stock -= ticket_data.stock
        else:
            game.stock += ticket_data.stock
            game.sold_out = False
    

    if game.stock == 0:
        game.sold_out = True 
    else:
        game.sold_out = False      
        
    session.add(game)
    session.commit()
    session.refresh(game)
    
    return game, there_stock