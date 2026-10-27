"""Portfolio Optimization & Capital Allocation Agent.
Balances expected ROI, CapEx constraints, and risk appetite across retail store candidates.
"""

import logging
import os
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.portfolio import (
    LocationCandidate,
    PortfolioRequest,
    PortfolioResponse,
    SelectedLocation,
)

logger = logging.getLogger("retailmind.portfolio_agent")

router = APIRouter(prefix="/portfolio", tags=["Portfolio Optimization"])

PORTFOLIO_AGENT_SYSTEM_PROMPT = """
You are RetailMind's Chief Investment & Portfolio Strategy Agent.
Your role is to formulate capital allocation strategies across multi-store retail expansion candidates,
balancing risk tolerance, CapEx budgets, and return on invested capital.
"""


def optimize_portfolio_allocation(req: PortfolioRequest) -> PortfolioResponse:
    """Greedy/Knapsack heuristic for capital allocation constrained by total budget and risk tolerance."""
    budget_available = req.total_budget
    risk_profile = req.risk_tolerance.lower().strip()

    # Risk penalties/weights
    risk_weights = {
        "conservative": {"low": 1.2, "medium": 0.8, "high": 0.2},
        "moderate": {"low": 1.0, "medium": 1.0, "high": 0.8},
        "aggressive": {"low": 0.8, "medium": 1.1, "high": 1.3},
    }
    weights = risk_weights.get(risk_profile, risk_weights["moderate"])

    # Rank candidates by risk-adjusted return ratio
    def score_candidate(cand: LocationCandidate) -> float:
        risk_key = cand.risk_level.lower()
        multiplier = weights.get(risk_key, 1.0)
        # Ratio of annual net profit to required CapEx
        annual_profit = cand.expected_annual_revenue - cand.expected_annual_costs
        ratio = (annual_profit / cand.capex_required) if cand.capex_required > 0 else 0
        return ratio * multiplier

    sorted_candidates = sorted(req.candidates, key=score_candidate, reverse=True)

    selected: List[SelectedLocation] = []
    deferred_ids: List[str] = []
    current_allocated = 0.0

    for cand in sorted_candidates:
        # Check max locations constraint
        if req.max_locations is not None and len(selected) >= req.max_locations:
            deferred_ids.append(cand.id)
            continue

        annual_profit = round(cand.expected_annual_revenue - cand.expected_annual_costs, 2)
        if cand.capex_required <= (budget_available - current_allocated):
            current_allocated += cand.capex_required
            selected.append(
                SelectedLocation(
                    candidate_id=cand.id,
                    name=cand.name,
                    allocated_capex=cand.capex_required,
                    expected_annual_revenue=cand.expected_annual_revenue,
                    expected_annual_profit=annual_profit,
                    expected_roi_pct=cand.expected_roi_pct,
                    risk_level=cand.risk_level,
                    selection_rationale=(
                        f"Approved for deployment: strong risk-adjusted ROI ({cand.expected_roi_pct}%) "
                        f"and fits available capital."
                    ),
                )
            )
        else:
            deferred_ids.append(cand.id)

    remaining_budget = round(budget_available - current_allocated, 2)
    current_allocated = round(current_allocated, 2)

    total_profit = round(sum(s.expected_annual_profit for s in selected), 2)
    portfolio_roi = (
        round((total_profit / current_allocated) * 100.0, 2)
        if current_allocated > 0
        else 0.0
    )

    strategic_rationale = (
        f"Capital allocation optimized for a '{req.risk_tolerance}' investment thesis. "
        f"Greenlit {len(selected)} of {len(req.candidates)} candidate locations, committing "
        f"${current_allocated:,.2f} ({round((current_allocated/budget_available)*100, 1)}% of total budget) "
        f"with an aggregate projected annual profit of ${total_profit:,.2f} "
        f"and weighted portfolio ROI of {portfolio_roi}%. Reserve liquidity retained: ${remaining_budget:,.2f}."
    )

    return PortfolioResponse(
        total_budget=req.total_budget,
        allocated_budget=current_allocated,
        remaining_budget=remaining_budget,
        selected_locations=selected,
        deferred_locations=deferred_ids,
        portfolio_roi_pct=portfolio_roi,
        total_projected_annual_profit=total_profit,
        portfolio_risk_rating=req.risk_tolerance.capitalize(),
        strategic_rationale=strategic_rationale,
    )


@router.post(
    "/optimize",
    response_model=PortfolioResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize retail expansion capital allocation",
    description="Allocates capital budget across candidate store locations to maximize portfolio return within risk appetite.",
)
async def optimize_portfolio(request: PortfolioRequest) -> PortfolioResponse:
    """Endpoint for portfolio optimization and capital allocation."""
    try:
        return optimize_portfolio_allocation(request)
    except Exception as exc:
        logger.error("Error during portfolio optimization: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization failed: {str(exc)}",
        )
