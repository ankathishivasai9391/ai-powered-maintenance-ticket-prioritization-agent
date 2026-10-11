# ðŸ”§ AI-Powered Maintenance Ticket Prioritization Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/TF--IDF-NLP-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Railway-Deployed-0B0D0E?style=for-the-badge&logo=railway&logoColor=white"/>
</p>

<p align="center">
  <strong>An AI agent that classifies, scores, and routes renewable-energy maintenance tickets â€” with a live web dashboard, full REST API, and benchmark evaluation panel.</strong>
</p>

<p align="center">
  <a href="https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/">ðŸš€ Live Dashboard</a> Â·
  <a href="https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/docs">ðŸ“– API Docs (Swagger)</a> Â·
  <a href="https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/health">â¤ï¸ Health Check</a>
</p>

---

## ðŸ“‹ Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start â€” Run Locally](#quick-start--run-locally)
- [Run with VS Code](#-run-with-vs-code-one-click)
- [Environment Configuration](#environment-configuration)
- [API Reference](#api-reference)
- [Evaluation Results](#evaluation-results)
- [Testing](#testing)
- [Cloud Deployment](#cloud-deployment)
- [Limitations & Roadmap](#limitations--roadmap)
- [Author](#author)

---

## Overview

Maintenance teams at renewable energy facilities (wind turbines, solar inverters, SCADA systems) receive dozens of fault reports daily. Manual triage is slow, inconsistent, and risks missing critical failures.

This project delivers an **AI-powered prioritization agent** that:

1. **Classifies** each ticket into a maintenance category (e.g., `gearbox_vibration`, `inverter_thermal`, `pitch_system`)
2. **Estimates severity** (`low` / `medium` / `high` / `critical`) using a hybrid NLP + rule-based engine
3. **Calculates a priority score** (0â€“100) with a transparent breakdown
4. **Recommends the correct maintenance team** and suggests the next action
5. **Persists tickets** in SQLite and surfaces them in a live web dashboard

> **Human-in-the-loop principle:** The agent provides decision support. A qualified engineer must approve safety-critical actions before execution.

---

## Live Demo

| Resource | URL |
|:---|:---|
| ðŸŒ **Web Dashboard** | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/ |
| ðŸ“– **Swagger / OpenAPI** | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/docs |
| â¤ï¸ **Health Check** | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/health |

---

## Key Features

| Feature | Description |
|:---|:---|
| ðŸ§  **AI Ticket Analysis** | TF-IDF cosine similarity + hybrid rule-based expert engine |
| ðŸ“Š **Priority Scoring** | Transparent 0â€“100 score with a step-by-step breakdown |
| ðŸ—‚ **Category Classification** | 10 renewable-energy maintenance categories |
| âš¡ **Severity Estimation** | Four-level severity with keyword and context signals |
| ðŸ‘¥ **Team Routing** | Automatic assignment to the best-fit maintenance team |
| ðŸ–¥ **Live Dashboard** | Browser-based queue manager with filtering, search, and modals |
| ðŸ”Œ **REST API** | Full CRUD + analysis endpoints with OpenAPI docs |
| ðŸ“ˆ **Evaluation Panel** | Live benchmark accuracy metrics on the dashboard |
| ðŸ’¾ **SQLite Persistence** | Lightweight embedded database â€” zero infrastructure overhead |
| ðŸ³ **Docker Ready** | One-command containerised build and run |
| ðŸ§ª **Test Suite** | Unit, integration, and end-to-end API tests |

---

## How It Works

```text
 User submits maintenance description (via Dashboard or API)
                         â”‚
                         â–¼
              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
              â”‚   FastAPI Backend   â”‚
              â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â”‚
           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
           â”‚  Preprocessing Layer   â”‚
           â”‚  Â· Text normalisation  â”‚
           â”‚  Â· Keyword extraction  â”‚
           â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â”‚
           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
           â”‚  TF-IDF Vectorizer     â”‚  â† scikit-learn (pure-Python fallback)
           â”‚  + Cosine Similarity   â”‚
           â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â”‚
           â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
           â”‚  Hybrid Rule Engine    â”‚
           â”‚  Â· Category mapping    â”‚
           â”‚  Â· Severity scoring    â”‚
           â”‚  Â· Priority formula    â”‚
           â”‚  Â· Team assignment     â”‚
           â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â”‚
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â”‚                          â”‚
          â–¼                          â–¼
   Web Dashboard               SQLite Database
   (live ticket queue)         (persistent store)
```

---

## Technology Stack

| Layer | Technology |
|:---|:---|
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **NLP / AI** | TF-IDF Vectorizer, Cosine Similarity, Hybrid Rule-Based Expert System |
| **API Docs** | OpenAPI 3.0 / Swagger UI (auto-generated) |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES2022) |
| **Database** | SQLite via Python `sqlite3` |
| **Testing** | pytest, httpx, custom e2e API runner |
| **Containerisation** | Docker (python:3.12-slim) |
| **Deployment** | Railway (production) |
| **CI / Versioning** | Git + GitHub |

---

## Project Structure

```text
ai-powered-maintenance-ticket-prioritization-agent/
â”‚
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app.py              # FastAPI application, all route handlers
â”‚   â”œâ”€â”€ agent.py            # Core AI agent â€” TF-IDF, rules, scoring
â”‚   â”œâ”€â”€ database.py         # SQLite CRUD layer
â”‚   â”œâ”€â”€ schemas.py          # Pydantic request / response models
â”‚   â””â”€â”€ config.py           # Path constants and app settings
â”‚
â”œâ”€â”€ frontend/
â”‚   â””â”€â”€ index.html          # Single-page dashboard (HTML + CSS + JS)
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ test_agent.py       # Unit tests for the AI agent logic
â”‚   â”œâ”€â”€ test_api.py         # Integration tests for API endpoints
â”‚   â””â”€â”€ test_database.py    # Database CRUD tests
â”‚
â”œâ”€â”€ data/
â”‚   â””â”€â”€ maintenance_tickets.csv   # Labeled benchmark dataset (6 samples)
â”‚
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ ARCHITECTURE.md     # Technical design decisions
â”‚   â””â”€â”€ API_EXAMPLES.md     # cURL / Python API usage examples
â”‚
â”œâ”€â”€ e2e_test.py             # End-to-end live API test runner
â”œâ”€â”€ requirements.txt        # Python dependencies (pinned)
â”œâ”€â”€ Dockerfile              # Container build spec (python:3.12-slim)
â”œâ”€â”€ railway.json            # Railway deployment configuration
â”œâ”€â”€ Procfile                # Process declaration for PaaS runners
â”œâ”€â”€ .env.example            # Environment variable template
â”œâ”€â”€ .gitignore              # Excludes venvs, DBs, secrets, caches
â”œâ”€â”€ EVALUATION.md           # Benchmark methodology and results
â”œâ”€â”€ DEMO_NOTES.md           # Quick reviewer demonstration guide
â””â”€â”€ LIMITATIONS_AND_ROADMAP.md   # Honest constraints and future work
```

---

## Quick Start â€” Run Locally

### Prerequisites
- Python 3.12+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
cd ai-powered-maintenance-ticket-prioritization-agent
```

### 2. Create and activate a virtual environment

```powershell
# Windows (PowerShell)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the server

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Open in your browser

| Resource | URL |
|:---|:---|
| ðŸŒ Dashboard | http://127.0.0.1:8000/ |
| ðŸ“– Swagger UI | http://127.0.0.1:8000/docs |
| â¤ï¸ Health Check | http://127.0.0.1:8000/api/health |

> **Tip:** Click **"Reset / Seed Benchmark Dataset"** in the dashboard header to pre-load sample tickets on first run.

---

## 💻 Run with VS Code (One-Click)

This repository includes pre-configured `.vscode/` settings, debuggers, and tasks for a zero-configuration developer experience.

> 📖 **Full Deep-Dive Guide:** For in-depth extension recommendations, shortcut cheatsheets, troubleshooting, and CI/CD workflow, see [docs/VSCODE_SETUP_GUIDE.md](docs/VSCODE_SETUP_GUIDE.md).

### 1. Open the Project
```powershell
code d:\ai-powered-maintenance-ticket-prioritization-agent
```

### 2. Select Interpreter
- Press `Ctrl + Shift + P`
- Type: `Python: Select Interpreter`
- Choose: `.venv` (Python 3.12.x)

### 3. Run & Debug via `F5`
Press **`F5`** or go to **Run and Debug** (`Ctrl + Shift + D`):
- **`🚀 FastAPI Server (Dev)`** — Launches the server at `http://127.0.0.1:8000` with hot-reload enabled.
- **`🧪 Run All Tests`** — Executes `pytest tests/ -v` inside the VS Code debugger.
- **`🌐 E2E API Test`** — Executes the complete 28-point end-to-end API test suite (`e2e_test.py`).

### 4. Run Pre-Configured Tasks
Press `Ctrl + Shift + P` → select **Tasks: Run Task**:
| Task | Description |
|:---|:---|
| `🚀 Start Dev Server` | Runs uvicorn with live reload |
| `🧪 Run All Tests` | Runs pytest with verbose reporting |
| `🌐 Run E2E Tests` | Runs full live API suite |
| `📦 Install Dependencies` | Runs `pip install -r requirements.txt` |
| `🐳 Docker Build` | Builds local Docker image |
| `🐳 Docker Run` | Runs container on port 8000 |
| `🔄 Git Push to Deploy` | Pushes to GitHub & triggers Railway deploy |

---

## Environment Configuration

Copy the template and configure as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|:---|:---|:---|
| `PORT` | `8000` | HTTP port (auto-set by Railway/Render) |
| `DB_PATH` | `tickets.db` | SQLite database file path |

No external API keys are required. The agent runs fully offline.

---

## API Reference

| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/` | Serves the web dashboard |
| `GET` | `/api/health` | Service + database health check |
| `GET` | `/api/demo` | Starter scenario metadata |
| `POST` | `/api/analyze` | Analyze a ticket (no persistence) |
| `POST` | `/api/tickets` | Create + persist a new ticket |
| `GET` | `/api/tickets` | List all tickets (filter/search/paginate) |
| `GET` | `/api/tickets/{id}` | Get single ticket details |
| `PATCH` | `/api/tickets/{id}/status` | Update workflow status |
| `PATCH` | `/api/tickets/{id}/assign` | Reassign to another team |
| `DELETE` | `/api/tickets/{id}` | Delete a ticket |
| `GET` | `/api/metrics` | Dashboard KPI metrics |
| `GET` | `/api/evaluation` | Live benchmark accuracy results |
| `POST` | `/api/seed` | Re-seed database with benchmark data |

Full interactive docs available at `/docs` (Swagger UI).
See [`docs/API_EXAMPLES.md`](docs/API_EXAMPLES.md) for cURL and Python request examples.

---

## Evaluation Results

Evaluated against the labeled benchmark dataset (`data/maintenance_tickets.csv`):

| Metric | Score | Detail |
|:---|:---|:---|
| **Category Accuracy** | **100.0%** | 6 / 6 correct |
| **Severity Accuracy** | **83.3%** | 5 / 6 correct |
| **Method** | TF-IDF Cosine Similarity + Hybrid Rule-Based Expert System | â€” |

> See [`EVALUATION.md`](EVALUATION.md) for the full confusion matrix, methodology, and per-ticket breakdown.

---

## Testing

### Unit + Integration tests

```bash
python -m pytest tests/ -v
```

### End-to-end API test (requires running server)

```bash
# Start server first, then in a second terminal:
python e2e_test.py
```

All tests use an isolated SQLite session and do not affect production data.

---

## Cloud Deployment

The application is deployed to **Railway** via Docker.

### Deploy your own fork to Railway

1. Fork this repository on GitHub
2. Go to [railway.app](https://railway.app) â†’ **New Project** â†’ **Deploy from GitHub repo**
3. Railway detects the `Dockerfile` automatically
4. Set environment variable: `PORT` = `8000` (Railway also injects this)
5. Done â€” your deployment URL appears in the dashboard

### Local Docker build

```bash
docker build -t ticket-agent .
docker run -p 8000:8000 -e PORT=8000 ticket-agent
```

---

## Limitations & Roadmap

See [`LIMITATIONS_AND_ROADMAP.md`](LIMITATIONS_AND_ROADMAP.md) for a full discussion.

**Key constraints:**
- Benchmark evaluated on 6 labeled samples (energy domain heuristics)
- No real-time SCADA/IoT sensor stream integration
- SQLite is not horizontally scalable (use PostgreSQL for production scale)
- No authentication layer on the current API

**Planned improvements:**
- Integrate an LLM (e.g., Gemini, GPT-4o) for richer root-cause narratives
- Real-time sensor anomaly detection via MQTT/WebSocket
- Role-based access control (RBAC) on the API
- Expand benchmark to 100+ labeled samples with cross-validation

---

## Author

**Shivasai Ankathi**
- ðŸ™ GitHub: [@ankathishivasai9391](https://github.com/ankathishivasai9391)
- ðŸ“¦ Repository: [ai-powered-maintenance-ticket-prioritization-agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

---

<p align="center">Built as an AI Engineering Assessment Â· Python Â· FastAPI Â· TF-IDF Â· Railway</p>

