# app/infrastructure/database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# URL de la base de datos (puede ir en variables de entorno)
DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5433/apiBrian"

# Crear el engine
engine = create_engine(DATABASE_URL, echo=True)


# Dependencia para obtener una sesión por request
def get_session():
    with Session(engine) as session:
        yield session
        # ⚠️ OJO: No haces commit aquí, dejas que lo haga tu servicio
        # así tenés más control y evitas commits innecesarios


# Para tipar las dependencias (más limpio en routers/servicios)
SessionDep = Annotated[Session, Depends(get_session)]


# Crear tablas (solo lo usas al inicio de la app)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
