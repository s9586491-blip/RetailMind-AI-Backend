# 🏬 RetailMind AI Backend

This directory contains the core backend services, FastAPI application, Antigravity AI agents, and Pydantic schemas for **RetailMind AI**.

> [!NOTE]
> For the complete documentation, architecture diagrams, and Replit integration guides, see the [Master Repository README](../README.md).

---

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env

# 3. Start development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Directory Outline
- `main.py`: Application entry point with Replit-friendly CORS middleware and versioned router bindings.
- `agents/`: Antigravity SDK agents (`location_agent.py`, `scenario_agent.py`, `portfolio_agent.py`).
- `models/`: Strictly typed Pydantic v2 schemas (`location.py`, `scenario.py`, `portfolio.py`, `common.py`).
- `test_client.py`: Automated verification suite for health checks, location scoring, simulations, and portfolio optimization.

## Interactive API Docs
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
