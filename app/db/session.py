import os
from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
load_dotenv()

IS_PROD_ENV = os.getenv("IS_PROD", "false").lower() == "true"
IS_RENDER = os.getenv("RENDER") is not None
IS_STRICKLY_PROD = IS_PROD_ENV or IS_RENDER

if IS_STRICKLY_PROD:
  
    raw_url = os.getenv("DATABASE_URL") 
    connect_args = {"sslmode": "require"}
else:
   
    raw_url = os.getenv("DATABASE_URL_DEV")
    connect_args = {}

if not raw_url:
    raise ValueError(f"Error: URL de base de datos no encontrada para {'PROD' if IS_STRICKLY_PROD else 'DEV'}")

if raw_url.startswith("postgres://"):
    final_url = raw_url.replace("postgres://", "postgresql://", 1)
else:
    final_url = raw_url

engine = create_engine(
    final_url, 
    echo=not IS_STRICKLY_PROD,
    connect_args=connect_args
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session