from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from app.utils import generate_uuid
from app.db import engine
from app.schemas import ticket_model
from app.api import router

app = FastAPI(title="{URL}/hospital/v1/operaciones/tickets", version="1.0.0", description="API para hacer operaciones nivel CRUD", swagger_ui_parameters={"operationsSorter": "method"}, openapi_url="/openapi.json", docs_url="/docs")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def custom_http_exeption_handler(request: Request, exc: HTTPException):
    folio = generate_uuid()
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"folio": folio, "mensaje": str(exc.detail)},
        headers=exc.headers
    )
    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
app.include_router(router)