"""Automated verification script for RetailMind AI Backend and Antigravity Agents.
"""
import httpx

BASE_URL = "http://localhost:8000/api/v1"

def test_system():
    print("=== Testing System Health ===")
    r = httpx.get("http://localhost:8000/health")
    print(r.json())
    print()

def test_location_scoring():
    print("=== Testing Location Intelligence Agent (Antigravity) ===")
    payload = {
        "area_name": "SoHo, New York, NY",
        "target_demographic": "Gen-Z and millennial urbanites, high disposable income",
        "store_category": "Athleisure & Performance Apparel",
        "store_size_sqft": 2500,
        "monthly_rent_budget": 22000.0
    }
    r = httpx.post(f"{BASE_URL}/locations/score", json=payload)
    data = r.json()
    print(f"Score: {data.get('score')}/100")
    print(f"Recommendation: {data.get('recommendation_summary')}")
    print(f"Pros: {data.get('pros')}")
    print()

def test_scenario_simulation():
    print("=== Testing What-If Scenario Simulation ===")
    payload = {
        "scenario_name": "Q3 Prime Expansion & Foot Traffic Lift",
        "baseline_revenue": 1200000.0,
        "baseline_costs": 850000.0,
        "cost_change_pct": 5.0,
        "conversion_rate_shift_pct": 12.5,
        "time_horizon_months": 12
    }
    r = httpx.post(f"{BASE_URL}/scenarios/simulate", json=payload)
    data = r.json()
    print(f"Projected Net Profit: ${data.get('projected_net_profit'):,.2f}")
    print(f"Net Impact: ${data.get('net_impact'):,.2f} ({data.get('net_impact_pct'):+.1f}%)")
    print(f"Summary: {data.get('summary')}")
    print()

def test_portfolio_optimization():
    print("=== Testing Portfolio Capital Optimization ===")
    payload = {
        "total_budget": 1000000.0,
        "risk_tolerance": "moderate",
        "candidates": [
            {
                "id": "LOC-01",
                "name": "Downtown Flagship",
                "capex_required": 350000.0,
                "expected_annual_revenue": 1400000.0,
                "expected_annual_costs": 980000.0,
                "expected_roi_pct": 120.0,
                "risk_level": "medium",
                "store_format": "Flagship"
            },
            {
                "id": "LOC-02",
                "name": "Suburban Mall Boutique",
                "capex_required": 200000.0,
                "expected_annual_revenue": 750000.0,
                "expected_annual_costs": 500000.0,
                "expected_roi_pct": 125.0,
                "risk_level": "low",
                "store_format": "Boutique"
            }
        ]
    }
    r = httpx.post(f"{BASE_URL}/portfolio/optimize", json=payload)
    data = r.json()
    print(f"Allocated Budget: ${data.get('allocated_budget'):,.2f} / ${data.get('total_budget'):,.2f}")
    print(f"Selected Locations: {len(data.get('selected_locations'))}")
    print(f"Strategic Rationale: {data.get('strategic_rationale')}")
    print()

if __name__ == "__main__":
    print("Starting automated RetailMind AI verification...\n")
    try:
        test_system()
        test_location_scoring()
        test_scenario_simulation()
        test_portfolio_optimization()
        print("All automated tests completed successfully!")
    except Exception as e:
        print(f"Test failed: Ensure your backend is running via `python main.py`. Error: {e}")