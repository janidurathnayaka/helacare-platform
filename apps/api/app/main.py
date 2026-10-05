import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Source-grounded API for Sri Lankan indigenous health knowledge.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    path = request.url.path
    REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
    return response


app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    return {
        "name": "HelaCare API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": f"{settings.api_prefix}/health",
        "metrics": "/metrics",
    }
