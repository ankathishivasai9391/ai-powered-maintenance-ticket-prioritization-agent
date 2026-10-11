# AI-Powered Maintenance Ticket Prioritization Agent

An AI-assisted maintenance ticket management application that classifies incoming maintenance requests, estimates severity and priority, and recommends the team best suited to handle each ticket. It includes a web dashboard, REST API, evaluation metrics, and a lightweight database-backed workflow.

<p align="center">
  <strong>FastAPI · Python · TF-IDF Similarity · Hybrid Rule-Based Reasoning · SQLite · HTML/CSS/JavaScript · Render / Railway</strong>
</p>

<p align="center">
  <a href="https://onrender.com">Live Dashboard</a> · 
  <a href="https://onrender.comdocs">API Documentation</a> · 
  <a href="https://onrender.comapi/health">Health Check</a>
</p>

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Run Locally in VS Code](#run-locally-in-vs-code)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Evaluation](#evaluation)
- [Testing](#testing)
- [Cloud Deployment](#cloud-deployment)
- [Troubleshooting](#troubleshooting)
- [Limitations and Responsible Use](#limitations-and-responsible-use)
- [Future Improvements](#future-improvements)

---

## Overview

Maintenance teams receive requests involving equipment failures, inspections, electrical issues, HVAC problems, and other facility concerns. Manually reviewing and routing every request can delay work and lead to inconsistent prioritization.

This project provides an AI-assisted workflow that takes a maintenance ticket as input and returns structured prioritization information, such as:
- Predicted maintenance category
- Estimated severity
- Priority score
- Recommended maintenance team
- API-backed ticket and dashboard information

> **Important:** The system provides decision support. A qualified maintenance professional should review safety-critical recommendations before acting on them.

---

## Key Features

- **Ticket analysis:** Analyze maintenance descriptions and return structured results.
- **Category prediction:** Match a ticket against known maintenance categories.
- **Severity estimation:** Apply the application's hybrid analysis logic to estimate urgency.
- **Priority scoring:** Produce a numeric priority score to help sort incoming requests.
- **Team recommendation:** Suggest a maintenance team based on ticket details.
- **Web dashboard:** View and interact with the application through a browser.
- **REST API:** Access backend operations through documented HTTP endpoints.
- **Evaluation panel:** Display benchmark category and severity validation results.
- **Database integration:** Store ticket data using SQLite.
- **Similarity fallback:** Includes a pure-Python similarity fallback if optional C-extensions are unavailable.
- **Automated tests:** Includes unit/integration tests and an end-to-end API test script.

---

## How It Works

```text
User submits a maintenance request
                │
                ▼
         FastAPI backend
                │
                ▼
     Input processing & analysis
                │
                ▼
  TF-IDF similarity + hybrid rule-based logic
                │
                ▼
  Category, severity, priority score,
  and recommended maintenance team
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
 Web dashboard     SQLite database
       │
       ▼
 User reviews recommendation
```

---

## Technology Stack

| Area | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, Uvicorn |
| **API Docs** | OpenAPI / Swagger UI |
| **Text Analysis** | TF-IDF & Cosine Similarity (with pure-Python fallback) |
| **Decision Logic** | Hybrid Rule-Based Maintenance Analysis |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite |
| **Testing** | pytest & custom e2e API script |
| **Deployment** | Docker, Render / Railway |

---

## Project Structure

```text
ai-powered-maintenance-ticket-prioritization-agent/
├── backend/
│   ├── app.py              # FastAPI application and routes
│   └── agent.py            # Ticket analysis and prioritization logic
├── frontend/
│   └── index.html          # Interactive browser dashboard
├── tests/                  # Unit and integration test suite
├── data/                   # Local database and seed CSV datasets
├── requirements.txt        # Python package dependencies
├── e2e_test.py             # End-to-end API test runner
├── Dockerfile              # Container build specifications
├── nixpacks.toml           # Nixpacks build configuration (if used)
├── railway.json            # Railway deployment config (if used)
└── README.md               # Project documentation
```

---

## Run Locally in VS Code

### 1. Prerequisites
- Python 3.12+
- Visual Studio Code & Git

### 2. Clone the repository
```bash
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
cd ai-powered-maintenance-ticket-prioritization-agent
```

### 3. Create a virtual environment
```powershell
# Windows PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the application
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Access local URLs

| Resource | Local URL |
| :--- | :--- |
| **Dashboard** | http://127.0.0.1:8000/ |
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **Health Check** | http://127.0.0.1:8000/api/health |

*Press `Ctrl + C` in the terminal to stop the server.*

---

## Configuration

Environment variables recognized by the app:
- `PORT` : HTTP port assigned by hosting provider (defaults to `8000` locally).
- `DB_PATH` : Custom file path for SQLite storage.

---

## API Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `GET` | `/` | Serves web dashboard |
| `GET` | `/api/health` | Reports service and DB health status |
| `GET` | `/api/demo` | Returns sample/starter scenario metadata |
| `GET` | `/api/metrics` | Returns ticket counts and evaluation rubrics |
| `POST` | `/api/analyze` | Evaluates text input and returns real-time triage |
| `POST` | `/api/tickets` | Creates and persists a new maintenance ticket |

---

## Evaluation

Benchmark metrics evaluated against labeled sample set (`maintenance_tickets.csv`):
- **Category Accuracy**: `100.0%` (6/6)
- **Severity Accuracy**: `83.3%` (5/6)

> *Note: Measured on a 6-item reference benchmark. Evaluate on an expanded domain dataset before enterprise deployment.*

---

## Testing

Run unit and integration tests:
```bash
python -m pytest tests/ -v
```

Run end-to-end API verification:
```bash
python e2e_test.py
```

---

## Cloud Deployment

### Deploying to Render
1. Push your repository to GitHub.
2. Create a new **Web Service** on Render and connect your repo.
3. Set **Runtime** to `Docker`.
4. Add environment variable: `PORT` = `8000`.

### Deploying to Railway
1. Connect your GitHub repository.
2. Ensure start command uses: `uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-8000}`.
3. Attach a persistent volume if SQLite state needs to survive redeployments.

---

## Troubleshooting

- **Import Errors / Missing C-libs**: Ensure `Dockerfile` includes system libraries (`libgomp1`) or use the fallback pure-Python vectorizer.
- **Port In Use**: Switch to port 8001 (`--port 8001`).
- **Empty Queue on Load**: Click **`🔄 Reset / Seed Benchmark Dataset`** in the UI header to populate initial database records.

---

## Limitations and Responsible Use
- Small sample evaluation size.
- Dependent on quality of descriptive text and domain rules.
- Decision support tool—human review required for critical or hazardous operations.

---

## Author

**Shivasai Ankathi**  
- GitHub: [ankathishivasai9391](https://github.com/ankathishivasai9391)  
- Repository: [ai-powered-maintenance-ticket-prioritization-agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)
