"""
D5 - Rédacteur de Rapports Intelligent
Application FastAPI avec OpenAI, Qdrant et SearxNG
"""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes.reports import router as reports_router
from routes.data import router as data_router
from routes.export import router as export_router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Démarrage de l'application sur http://localhost:{settings.PORT}")
    print(f"📡 OpenAI: {'✅' if settings.OPENAI_API_KEY else '❌'}")
    print(f"🔍 SearxNG: {settings.SEARXNG_URL}")
    print(f"🗄️  Qdrant: {settings.QDRANT_URL}")
    yield
    print("🛑 Arrêt de l'application")


app = FastAPI(
    title="D5 - Rédacteur de Rapports IA",
    description="Génération automatique de rapports structurés avec IA générative",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(reports_router, prefix="/api/reports", tags=["Rapports"])
app.include_router(data_router, prefix="/api/data", tags=["Données"])
app.include_router(export_router, prefix="/api/export", tags=["Export"])

# Root page
from fastapi import Request
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "app": "D5 Rapport Generator"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
