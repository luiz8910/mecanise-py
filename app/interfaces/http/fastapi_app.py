from fastapi import FastAPI
from ..infrastructure.persistence.db import init_db
from .routers.webhook import router as webhook_router

app = FastAPI(title="Mecanice", version="0.1.0")


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/healthz")
def healthz():
    return {"ok": True}


# Rotas
app.include_router(webhook_router)
