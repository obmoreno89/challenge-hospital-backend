import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from sqlmodel import Session
from app.schemas import TicketTable
from fastapi import HTTPException, status, UploadFile
from app.utils import generate_uuid
from datetime import datetime

load_dotenv()

cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

def post_ticket(session: Session, asunto: str, prioridad: int, detalle: str, archivo: UploadFile):
    folio = generate_uuid()
    
    try:
        upload_result = cloudinary.uploader.upload(archivo.file, resource_type="auto", folder="hospital_tickets")
        archivo_url = upload_result.get("secure_url")

        new_ticket = TicketTable(
            asunto=asunto,
            prioridad=prioridad,
            detalle=detalle,
            archivo_url=archivo_url,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
            estatus=1
        )
        
        session.add(new_ticket)
        session.commit()
        session.refresh(new_ticket)
        return new_ticket
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"folio": folio, "mensaje": "No se pudo guardar el archivo o el ticket"}
        )