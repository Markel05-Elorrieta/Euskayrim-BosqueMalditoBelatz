from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.app.database import Base, engine
from api.app.ml.model_loader import ModelLoader
from api.app.models import orm as _orm_models
from api.app.routers import health, heroes, whatif, divine


# --- Crear tablas + cargar modelo ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ModelLoader.load()
    yield


app = FastAPI(
    title="Reto Final - Markel y Arian - Euskayrim",
    description="API del reto final de Euskayrim",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(heroes.router)
app.include_router(whatif.router)
app.include_router(divine.router)

# EL FRONTEND
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")


@app.get("/")
def home():
    return {"mensaje": "Bienvenido al FastAPI del reto de Euskayrim. Visita /docs para la documentación de la API. Un saludo!"}