# app/infrastructure/database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from app.core.config import settings

# URL de la base de datos (puede ir en variables de entorno)
# DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5433/apiBrian"
DATABASE_URL=f"postgresql+psycopg2://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
# Crear el engine
engine = create_engine(DATABASE_URL, echo=True)


# Dependencia para obtener una sesión por request 
def get_session():
    with Session(engine) as session:
        yield session
    #no hace commit, lo hace el servicio    


# Para tipar las dependencias (más limpio en routers/servicios)
SessionDep = Annotated[Session, Depends(get_session)]


# Crear tablas (solo lo usas al inicio de la app)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
