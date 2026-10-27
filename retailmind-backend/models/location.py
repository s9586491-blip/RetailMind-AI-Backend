"""Pydantic schemas for location scoring and demographic demand analysis.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class LocationRequest(BaseModel):
    """Input payload for evaluating store location suitability and demographic demand."""

    area_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Name or geographic designation of the target area, neighborhood, or trade zone",
        examples=["SoHo, New York, NY", "Silver Lake, Los Angeles, CA"]
    )
    target_demographic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Target customer segment, behavioral traits, and demographic profile",
        examples=["Gen-Z and millennial urbanites, high disposable income, active lifestyle"]
    )
    store_category: Optional[str] = Field(
        default="Specialty Retail",
        max_length=100,
        description="Type or vertical of the retail store",
        examples=["Athleisure & Performance Apparel", "Artisanal Specialty Coffee"]
    )
    store_size_sqft: Optional[int] = Field(
        default=2500,
        ge=100,
        le=500000,
        description="Planned retail footprint in square feet",
        examples=[2500]
    )
    monthly_rent_budget: Optional[float] = Field(
        default=None,
        ge=0,
        description="Optional maximum monthly lease budget in USD",
        examples=[22000.0]
    )


class LocationResponse(BaseModel):
    """Structured output for retail location scoring and expansion viability."""

    area_name: str = Field(
        ...,
        description="The evaluated target area"
    )
    target_demographic: str = Field(
        ...,
        description="The evaluated customer demographic"
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Viability and market potential score bounded from 0 (poor) to 100 (prime)"
    )
    pros: List[str] = Field(
        ...,
        description="Key competitive advantages, foot traffic drivers, and positive market indicators"
    )
    cons: List[str] = Field(
        ...,
        description="Key risks, competitive saturations, cost impediments, or logistical barriers"
    )
    recommendation_summary: str = Field(
        ...,
        description="Executive recommendation and strategic expansion verdict"
    )
    demographic_fit_level: Optional[str] = Field(
        default="High",
        description="Qualitative rating of demographic alignment (High, Moderate, Low)"
    )
    estimated_foot_traffic: Optional[str] = Field(
        default=None,
        description="Qualitative or quantitative foot traffic tier (e.g. Heavy Pedestrian, Moderate)"
    )
    competition_density: Optional[str] = Field(
        default=None,
        description="Assessment of competitor presence and category saturation"
    )
