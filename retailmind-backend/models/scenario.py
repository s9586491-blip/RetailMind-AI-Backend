"""Pydantic schemas for 'What-if' simulation engine and financial impact modeling.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    """Input parameters for retail 'What-if' operational and financial simulation."""

    scenario_name: Optional[str] = Field(
        default="Store Expansion Simulation",
        description="Descriptive name or title for this simulation scenario",
        examples=["Prime Location Expansion", "Supply Chain & Wage Hike Scenario"]
    )
    baseline_revenue: float = Field(
        ...,
        ge=0,
        description="Current or baseline periodic revenue in USD (e.g., annual or monthly)",
        examples=[1200000.0]
    )
    baseline_costs: float = Field(
        ...,
        ge=0,
        description="Current or baseline operational costs in USD for the corresponding period",
        examples=[850000.0]
    )
    cost_change_pct: float = Field(
        ...,
        ge=-100.0,
        le=500.0,
        description="Projected change in operational costs as a percentage (e.g. +7.5 for +7.5%, -4.0 for -4%)",
        examples=[6.0]
    )
    conversion_rate_shift_pct: float = Field(
        ...,
        ge=-100.0,
        le=500.0,
        description="Projected change in conversion rate or sales volume as a percentage (e.g. +12.0 for +12%)",
        examples=[15.0]
    )
    time_horizon_months: Optional[int] = Field(
        default=12,
        ge=1,
        le=120,
        description="Projection horizon in months",
        examples=[12]
    )


class ScenarioResponse(BaseModel):
    """Calculated projections and net impact from a 'What-if' scenario."""

    scenario_name: str = Field(
        ...,
        description="Name of the evaluated simulation"
    )
    baseline_revenue: float = Field(
        ...,
        description="Initial baseline revenue in USD"
    )
    baseline_costs: float = Field(
        ...,
        description="Initial baseline operational costs in USD"
    )
    baseline_net_profit: float = Field(
        ...,
        description="Baseline net profit in USD (baseline_revenue - baseline_costs)"
    )
    projected_revenue: float = Field(
        ...,
        description="Projected revenue in USD following conversion rate shifts"
    )
    projected_costs: float = Field(
        ...,
        description="Projected operational costs in USD following cost shifts"
    )
    projected_net_profit: float = Field(
        ...,
        description="Projected net profit in USD (projected_revenue - projected_costs)"
    )
    net_impact: float = Field(
        ...,
        description="Absolute change in net profit in USD (projected_net_profit - baseline_net_profit)"
    )
    net_impact_pct: float = Field(
        ...,
        description="Percentage shift in net profit relative to baseline net profit"
    )
    baseline_margin_pct: float = Field(
        ...,
        description="Baseline operating profit margin percentage"
    )
    projected_margin_pct: float = Field(
        ...,
        description="Projected operating profit margin percentage"
    )
    summary: str = Field(
        ...,
        description="Executive summary and financial interpretation of the scenario outcome"
    )
    key_drivers: List[str] = Field(
        default_factory=list,
        description="Key operational or market factors driving the projected delta"
    )
