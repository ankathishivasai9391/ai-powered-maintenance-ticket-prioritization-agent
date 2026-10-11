# Architecture — AI-Powered Maintenance Ticket Prioritization Agent

## System Overview

The application follows a **monolithic single-process architecture** intentionally chosen for simplicity, low infrastructure cost, and ease of local development during the assessment period. All backend components run in a single Uvicorn process; the frontend is served as static HTML by FastAPI.

---

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                        │
│                                                          │
│   Browser (index.html)       External API Consumers      │
│   · Vanilla JS fetch()       · cURL / Postman / Python   │
│   · Dashboard UI             · Swagger UI (/docs)        │
└───────────────────┬─────────────────────┬────────────────┘
                    │ HTTP                │ HTTP
                    ▼                     ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI LAYER (app.py)                 │
│                                                          │
│  Route Handlers:                                         │
│  GET /            → Serve index.html                     │
│  POST /api/analyze → analyze_ticket()                    │
│  POST /api/tickets → create + persist ticket             │
│  GET  /api/tickets → list_tickets() with filters         │
│  PATCH /api/tickets/{id}/status → update status          │
│  GET  /api/evaluation → run benchmark evaluation         │
│  GET  /api/metrics  → dashboard KPIs                     │
│  GET  /api/health   → health check                       │
│  POST /api/seed     → seed benchmark data                │
└──────────┬───────────────────────────┬───────────────────┘
           │                           │
           ▼                           ▼
┌─────────────────────┐   ┌────────────────────────────────┐
│   AI AGENT LAYER    │   │      DATABASE LAYER             │
│   (agent.py)        │   │      (database.py)              │
│                     │   │                                  │
│  · TF-IDF Vectorize │   │  · init_db() — schema setup     │
│  · Cosine Similarity│   │  · save_ticket()                │
│  · Rule Engine      │   │  · list_tickets() + filters     │
│  · Priority Formula │   │  · get_ticket_by_id()           │
│  · Team Mapping     │   │  · update_ticket_status()       │
│  · evaluate_bench.. │   │  · get_metrics()                │
└─────────────────────┘   └──────────────┬─────────────────┘
                                         │
                                         ▼
                             ┌─────────────────────┐
                             │    SQLite DATABASE   │
                             │    (tickets.db)      │
                             └─────────────────────┘
```

---

## Component Deep Dive

### 1. `backend/app.py` — FastAPI Application

- Defines all HTTP routes using FastAPI decorators
- Mounts the `frontend/` directory as a static file server
- Handles CORS to allow local cross-origin development
- Runs `init_db()` at startup via the `lifespan` context manager
- Reads `PORT` from the environment at `__main__` time for Railway compatibility

### 2. `backend/agent.py` — AI Agent (Core)

The heart of the system. Contains the `TicketPrioritizationAgent` class with two main capabilities:

**Ticket Analysis Pipeline (`analyze_ticket`):**
```
Input description
    → preprocess_text()          # lowercase, strip punctuation
    → TfidfVectorizer.transform()  # vectorize input
    → cosine_similarity()        # compare vs. 10 category reference docs
    → top match = predicted category
    → hybrid_severity_rules()    # keyword + asset-type + context signals
    → compute_priority_score()   # base score + modifiers
    → map_team()                 # category → responsible team
    → build TicketAnalysisResponse
```

**Benchmark Evaluation (`evaluate_benchmark`):**
```
Load data/maintenance_tickets.csv
    → for each labeled row:
        → run analyze_ticket()
        → compare predicted vs. true category and severity
    → compute accuracy scores
    → return EvaluationResponse
```

**TF-IDF Fallback:**  
If `scikit-learn` is unavailable (e.g., missing `libgomp1` on some Linux builds), the agent falls back to a pure-Python TF-IDF implementation at the top of `agent.py`. This ensures the application always starts, even without compiled C extensions.

### 3. `backend/database.py` — SQLite CRUD

- Single connection function (`get_conn()`) pointing to `tickets.db`
- Schema: one `tickets` table with all analysis fields + workflow metadata
- `seed_db_from_csv()` loads `data/maintenance_tickets.csv` on demand
- Thread-safety: SQLite WAL mode is not enabled; use PostgreSQL for concurrent production writes

### 4. `backend/schemas.py` — Pydantic Models

Defines the data contracts for all API inputs and outputs:
- `TicketAnalysisRequest` — input with description, asset_type, asset_id
- `TicketAnalysisResponse` — full structured output including breakdown
- `TicketRecord` — persisted ticket with ID, timestamps, and status
- `EvaluationResponse` — benchmark accuracy metrics
- `MetricsResponse` — KPI counters for the dashboard

### 5. `frontend/index.html` — Single-Page Dashboard

A single-file frontend (HTML + CSS + JavaScript) served directly by FastAPI:
- **No build step required** — no npm, no bundler
- All API calls use the native `fetch()` API
- Design: vanilla CSS with custom properties, glassmorphism cards, responsive grid
- Ticket queue rendered dynamically from `/api/tickets`
- Evaluation panel reads from `/api/evaluation` on page load

---

## Key Design Decisions

| Decision | Rationale |
|:---|:---|
| **Single-file frontend** | Zero build toolchain complexity; served as static file from FastAPI |
| **SQLite over PostgreSQL** | Zero infrastructure overhead for assessment; trivial to swap via `DB_PATH` env var |
| **TF-IDF over LLM** | No API key required; fully offline; deterministic and auditable |
| **Pure-Python TF-IDF fallback** | Guarantees the app starts on any Python 3.12 environment regardless of C-extension availability |
| **Hybrid rule engine** | Domain expert knowledge is directly encodeable; transparent and debuggable |
| **Railway + Docker** | Reproducible deployments; `python:3.12-slim` gives a minimal attack surface |
| **Pydantic v2 schemas** | Auto-generates OpenAPI spec; runtime validation; clear API contracts |

---

## Data Flow for a Ticket Submission

```
1. User fills form → JS calls POST /api/tickets with JSON body
2. FastAPI validates body against TicketCreateRequest schema
3. agent.analyze_ticket(request) runs the full AI pipeline
4. TicketAnalysisResponse is returned from the agent
5. save_ticket(analysis) persists the record to SQLite
6. TicketRecord (with generated ticket_id + timestamps) is returned as HTTP 201
7. Frontend receives the response and refreshes the ticket queue table
```

---

## Security Considerations

| Concern | Current Status | Production Recommendation |
|:---|:---|:---|
| Authentication | ❌ None | Add JWT bearer via FastAPI OAuth2 |
| Input validation | ✅ Pydantic v2 | Already enforced |
| SQL injection | ✅ Parameterised queries | Already enforced |
| CORS | ⚠️ Allow-all (`*`) | Restrict to known origin domains |
| Secrets | ✅ `.env` excluded from git | Already enforced via `.gitignore` |

---

## Deployment Architecture (Railway)

```
GitHub push to main
        │
        ▼
Railway GitHub integration triggers build
        │
        ▼
Docker build: python:3.12-slim
  → apt-get install libgomp1
  → pip install -r requirements.txt
  → COPY source code
  → CMD: python backend/app.py
        │
        ▼
Uvicorn binds to 0.0.0.0:$PORT
Railway injects PORT environment variable
        │
        ▼
Public HTTPS URL exposed via Railway reverse proxy
```
