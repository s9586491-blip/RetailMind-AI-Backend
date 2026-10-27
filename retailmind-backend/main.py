"""RetailMind AI Backend - FastAPI Entry Point & Orchestration Hub.

Provides RESTful APIs for:
1. Location Scoring & Demographic Analysis (Google Antigravity Agent)
2. 'What-If' Financial and Operational Simulation Engine
3. Portfolio Capital Allocation & Store Investment Optimization
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project root to sys.path to ensure absolute and relative imports work smoothly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.location_agent import router as location_router
from agents.portfolio_agent import router as portfolio_router
from agents.scenario_agent import router as scenario_router
from models.common import APIErrorResponse, HealthResponse

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)
logger = logging.getLogger("retailmind.main")


# ---------------------------------------------------------------------------
# Lifespan Events
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown procedures."""
    logger.info("Initializing RetailMind AI Backend...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        logger.info("Google Antigravity SDK: GEMINI_API_KEY detected.")
    else:
        logger.warning(
            "GEMINI_API_KEY not detected. Agents will use local heuristic fallback engines."
        )
    yield
    logger.info("Shutting down RetailMind AI Backend...")


# ---------------------------------------------------------------------------
# FastAPI Application Initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="RetailMind AI Backend",
    description=(
        "Next-generation retail expansion, demographic demand scoring, "
        "and real-time financial simulation platform powered by Google Antigravity SDK."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS Configuration (Replit Frontend Support)
# ---------------------------------------------------------------------------
# Configurable via environment variable ALLOWED_ORIGINS (comma-separated).
# Supports all Replit app domains (*.replit.app, *.replit.dev, *.repl.co)
# and localhost development servers (Vite 5173, Next.js 3000, React 8080).
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    origins_list: List[str] = [origin.strip() for origin in env_origins.split(",") if origin.strip()]
else:
    # Default permissive origins for Replit and local development
    origins_list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://replit.com",
    ]

# Regex pattern matching any Replit workspace/deployment domain:
# e.g., https://retailmind-frontend.username.replit.app or .dev or .repl.co
REPLIT_ORIGIN_REGEX = (
    r"^https:\/\/([a-zA-Z0-9\-_]+\.)*(replit\.(app|dev)|repl\.co)$"
    r"|^http:\/\/localhost(:\d+)?$"
    r"|^http:\/\/127\.0\.0\.1(:\d+)?$"
)

# If wildcard is explicitly requested or in debug mode
if "*" in origins_list or os.getenv("CORS_ALLOW_ALL", "true").lower() == "true":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_list,
        allow_origin_regex=REPLIT_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ---------------------------------------------------------------------------
# Global Exception Handlers
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches unhandled errors and returns standardized JSON response."""
    logger.error("Unhandled exception processing %s %s: %s", request.method, request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIErrorResponse(
            detail=f"An unexpected server error occurred: {str(exc)}",
            error_code="INTERNAL_SERVER_ERROR",
        ).model_dump(mode="json"),
    )


# ---------------------------------------------------------------------------
# Health Check & Root Endpoints
# ---------------------------------------------------------------------------
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Service Health Check",
    description="Returns current API health, version, and server timestamp.",
)
async def health_check() -> HealthResponse:
    """Health-check endpoint for uptime monitoring and Replit pingers."""
    return HealthResponse(
        status="healthy",
        service="RetailMind AI Backend",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "production"),
    )


@app.get(
    "/",
    tags=["System"],
    summary="API Root Information",
    description="Welcome endpoint with system links and documentation endpoints.",
)
async def root():
    """Welcome payload with links to API documentation and active modules."""
    return {
        "service": "RetailMind AI Backend",
        "description": "Retail Expansion & Decision-Making Intelligence Platform",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json",
        },
        "endpoints": {
            "health": "/health",
            "location_scoring": "/api/v1/locations/score",
            "scenario_simulation": "/api/v1/scenarios/simulate",
            "portfolio_optimization": "/api/v1/portfolio/optimize",
        },
    }


# ---------------------------------------------------------------------------
# Router Inclusions
# ---------------------------------------------------------------------------
# Include under /api/v1 prefix (standardized API versioning)
app.include_router(location_router, prefix="/api/v1")
app.include_router(scenario_router, prefix="/api/v1")
app.include_router(portfolio_router, prefix="/api/v1")

# Also include directly at root for convenience and flexible frontend routing
app.include_router(location_router, include_in_schema=False)
app.include_router(scenario_router, include_in_schema=False)
app.include_router(portfolio_router, include_in_schema=False)


# ---------------------------------------------------------------------------
# Local Development Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
