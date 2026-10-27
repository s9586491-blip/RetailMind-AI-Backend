"""'What-If' Simulation Engine Agent.
Calculates financial and operational projections based on user inputs,
conversion rate shifts, and cost fluctuations in real-time.
"""

import logging
import os
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.scenario import ScenarioRequest, ScenarioResponse

logger = logging.getLogger("retailmind.scenario_agent")

router = APIRouter(prefix="/scenarios", tags=["Scenario Simulation"])

SCENARIO_AGENT_SYSTEM_PROMPT = """
You are RetailMind's Senior Financial & Retail Operations Analyst.
Your role is to analyze 'what-if' retail expansion scenarios, interpret sensitivity changes
in operational costs and conversion rates, and produce qualitative strategic commentary.
"""


def compute_simulation_projections(req: ScenarioRequest) -> ScenarioResponse:
    """Calculates deterministic projections based on conversion and cost shifts."""
    # Conversion rate shift directly scales revenue
    revenue_multiplier = 1.0 + (req.conversion_rate_shift_pct / 100.0)
    projected_revenue = round(req.baseline_revenue * revenue_multiplier, 2)

    # Cost change percentage scales operational costs
    cost_multiplier = 1.0 + (req.cost_change_pct / 100.0)
    projected_costs = round(req.baseline_costs * cost_multiplier, 2)

    # Profits
    baseline_profit = round(req.baseline_revenue - req.baseline_costs, 2)
    projected_profit = round(projected_revenue - projected_costs, 2)

    # Net impact
    net_impact = round(projected_profit - baseline_profit, 2)

    if baseline_profit != 0:
        net_impact_pct = round((net_impact / abs(baseline_profit)) * 100.0, 2)
    else:
        net_impact_pct = 100.0 if net_impact > 0 else (0.0 if net_impact == 0 else -100.0)

    # Margins
    baseline_margin = (
        round((baseline_profit / req.baseline_revenue) * 100.0, 2)
        if req.baseline_revenue > 0
        else 0.0
    )
    projected_margin = (
        round((projected_profit / projected_revenue) * 100.0, 2)
        if projected_revenue > 0
        else 0.0
    )

    # Key drivers identification
    drivers: List[str] = []
    if req.conversion_rate_shift_pct > 0:
        drivers.append(f"Top-line expansion driven by +{req.conversion_rate_shift_pct}% conversion lift")
    elif req.conversion_rate_shift_pct < 0:
        drivers.append(f"Top-line contraction from {req.conversion_rate_shift_pct}% conversion drop")

    if req.cost_change_pct > 0:
        drivers.append(f"Margin compression from +{req.cost_change_pct}% increase in operational expenses")
    elif req.cost_change_pct < 0:
        drivers.append(f"Operating leverage improvement through {abs(req.cost_change_pct)}% cost reduction")

    # Generate summary commentary
    if net_impact > 0:
        sentiment = "positive"
        recommendation = "Scenario yields accretive net profit growth and strong capital efficiency."
    elif net_impact == 0:
        sentiment = "neutral"
        recommendation = "Scenario results in neutral net profitability with no material margin expansion."
    else:
        sentiment = "adverse"
        recommendation = "Scenario exerts negative pressure on net margins; operational hedges recommended."

    summary = (
        f"{req.scenario_name}: Projected revenue is ${projected_revenue:,.2f} "
        f"vs baseline ${req.baseline_revenue:,.2f}. Projected costs are ${projected_costs:,.2f}. "
        f"Net financial impact is {('+' if net_impact >= 0 else '')}${net_impact:,.2f} "
        f"({('+' if net_impact_pct >= 0 else '')}{net_impact_pct}%). {recommendation}"
    )

    return ScenarioResponse(
        scenario_name=req.scenario_name or "Expansion Simulation",
        baseline_revenue=req.baseline_revenue,
        baseline_costs=req.baseline_costs,
        baseline_net_profit=baseline_profit,
        projected_revenue=projected_revenue,
        projected_costs=projected_costs,
        projected_net_profit=projected_profit,
        net_impact=net_impact,
        net_impact_pct=net_impact_pct,
        baseline_margin_pct=baseline_margin,
        projected_margin_pct=projected_margin,
        summary=summary,
        key_drivers=drivers,
    )


async def enrich_scenario_with_antigravity(
    req: ScenarioRequest, base_response: ScenarioResponse
) -> ScenarioResponse:
    """Optionally enriches scenario summary with Antigravity AI reasoning when API key is present."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return base_response

    try:
        from google.antigravity import Agent, LocalAgentConfig

        config = LocalAgentConfig(
            system_instructions=SCENARIO_AGENT_SYSTEM_PROMPT,
        )

        prompt = f"""
Provide a concise executive financial briefing (under 80 words) for this retail expansion simulation:
- Scenario: {req.scenario_name}
- Baseline Revenue: ${req.baseline_revenue:,.2f} | Costs: ${req.baseline_costs:,.2f}
- Conversion Shift: {req.conversion_rate_shift_pct}% | Cost Shift: {req.cost_change_pct}%
- Projected Revenue: ${base_response.projected_revenue:,.2f} | Projected Costs: ${base_response.projected_costs:,.2f}
- Net Profit Impact: ${base_response.net_impact:,.2f} ({base_response.net_impact_pct}%)
- Baseline Margin: {base_response.baseline_margin_pct}% -> Projected Margin: {base_response.projected_margin_pct}%

Give a sharp, decision-oriented insight on margin sensitivity and operational viability.
"""
        async with Agent(config=config) as agent:
            response = await agent.chat(prompt)
            ai_text = await response.text()
            if ai_text and len(ai_text.strip()) > 10:
                base_response.summary = ai_text.strip()

    except Exception as exc:
        logger.debug("Antigravity scenario commentary enrichment skipped: %s", exc)

    return base_response


@router.post(
    "/simulate",
    response_model=ScenarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Run real-time retail 'What-if' financial simulation",
    description="Calculates projected revenue, operational costs, net impact, and margin sensitivities.",
)
async def simulate_scenario(request: ScenarioRequest) -> ScenarioResponse:
    """Endpoint for real-time scenario simulation."""
    try:
        base_result = compute_simulation_projections(request)
        return await enrich_scenario_with_antigravity(request, base_result)
    except Exception as exc:
        logger.error("Error during scenario simulation: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(exc)}",
        )
