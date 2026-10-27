"""RetailMind Pydantic models package.
Exports schemas for location analysis, scenario simulation, portfolio optimization,
and standard API health and error responses.
"""

from .common import APIErrorResponse, HealthResponse
from .location import LocationRequest, LocationResponse
from .portfolio import (
    LocationCandidate,
    PortfolioRequest,
    PortfolioResponse,
    SelectedLocation,
)
from .scenario import ScenarioRequest, ScenarioResponse

__all__ = [
    # Common
    "HealthResponse",
    "APIErrorResponse",
    # Location
    "LocationRequest",
    "LocationResponse",
    # Scenario
    "ScenarioRequest",
    "ScenarioResponse",
    # Portfolio
    "LocationCandidate",
    "PortfolioRequest",
    "PortfolioResponse",
    "SelectedLocation",
]
