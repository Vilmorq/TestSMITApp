from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cargo_rate import router as cargo_router
from app.api.insurance import router as insurance_router
from app.core.exceptions import exception_handlers
from app.core.settings.api import api_settings
from app.core.settings.base import settings

app = FastAPI(**api_settings.model_dump(), exception_handlers=exception_handlers)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False, status_code=200)
async def check_health():
    return {"status": True}


app.include_router(
    cargo_router,
    prefix="/cargo-rate",
    tags=["cargo rates"],
)

app.include_router(
    insurance_router,
    prefix="/insurance",
    tags=["insurance"],
)
