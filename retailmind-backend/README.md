# RetailMind AI - Backend

**RetailMind** is an AI-powered retail expansion and decision-making platform designed to help retail operators, real estate teams, and executives evaluate store viability, model 'what-if' scenarios, and optimize capital allocation across candidate locations.

## Tech Stack
- **Framework**: FastAPI (`fastapi`, `uvicorn`)
- **Data Validation & Schemas**: Pydantic v2
- **Agentic AI Layer**: `google-antigravity` SDK (Gemini 3.8 Flash structured reasoning)
- **Frontend Target**: Replit React/Vite/Next.js frontend

---

## Directory Structure
```
retailmind-backend/
├── main.py                  # FastAPI application entry point & Replit CORS configuration
├── agents/                  # Antigravity agent & analytics modules
│   ├── __init__.py
│   ├── location_agent.py   # Store location scoring & demographic demand analysis
│   ├── scenario_agent.py   # 'What-If' simulation calculations & margin projections
│   └── portfolio_agent.py  # Capital allocation and portfolio optimization
├── models/                  # Pydantic v2 request/response schemas
│   ├── __init__.py         # Re-exports all schemas
│   ├── common.py           # Health check and standardized error responses
│   ├── location.py         # LocationRequest & LocationResponse
│   ├── scenario.py         # ScenarioRequest & ScenarioResponse
│   └── portfolio.py        # PortfolioRequest, LocationCandidate, PortfolioResponse
├── requirements.txt         # Python dependencies
└── .env.example             # Configuration template
```

---

## Getting Started

### 1. Install Dependencies
```bash
cd retailmind-backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> [!NOTE]
> If `GEMINI_API_KEY` is omitted, the backend automatically uses intelligent local heuristic engines for location scoring, scenario projections, and portfolio calculations, allowing frictionless testing.

### 3. Run the Development Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Core API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service uptime and status monitor |
| `GET` | `/` | Root information & API index |
| `POST` | `/api/v1/locations/score` | Location viability & demographic demand scoring |
| `POST` | `/api/v1/scenarios/simulate` | Real-time 'What-If' financial and operational simulation |
| `POST` | `/api/v1/portfolio/optimize` | Capital allocation and portfolio optimization |
| `GET` | `/docs` | Interactive Swagger UI documentation |

---

## Connecting to Replit Frontend
CORS is configured to accept requests from Replit preview URLs (`*.replit.app`, `*.replit.dev`, `*.repl.co`) as well as local development ports (`localhost:3000`, `localhost:5173`).
To connect your Replit frontend, set your frontend API base URL to your deployed backend URL or Replit backend URL (e.g. `VITE_API_URL=https://<your-backend-slug>.replit.app/api/v1`).
