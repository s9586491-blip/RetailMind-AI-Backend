"""Common Pydantic schemas for health checks, system status, and error reporting.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """System health and operational status response."""

    status: str = Field(
        default="healthy",
        description="Overall health status of the backend service",
        examples=["healthy"]
    )
    service: str = Field(
        default="RetailMind AI Backend",
        description="Service identifier",
        examples=["RetailMind AI Backend"]
    )
    version: str = Field(
        default="1.0.0",
        description="Current API release version",
        examples=["1.0.0"]
    )
    environment: str = Field(
        default="production",
        description="Active environment (development, staging, production)",
        examples=["production"]
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Current server UTC timestamp"
    )


class APIErrorResponse(BaseModel):
    """Standardized error response payload for API errors."""

    detail: str = Field(
        ...,
        description="Human-readable explanation of the error",
        examples=["Target area not found or could not be evaluated"]
    )
    error_code: str = Field(
        default="INTERNAL_SERVER_ERROR",
        description="Machine-readable error category",
        examples=["AGENT_EXECUTION_ERROR"]
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the error occurred"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional additional context or diagnostic details"
    )
