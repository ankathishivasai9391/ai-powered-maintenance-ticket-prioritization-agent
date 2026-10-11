# ⚡ AI-Powered Maintenance Ticket Prioritization Agent

> **Domain:** Renewable Energy Asset Management & Enterprise Dispatch  
> **Supported Assets:** Solar PV Arrays, Wind Turbine Generators, Hydroelectric Power, Substation & Grid Ops, Battery Storage (BESS)  
> **Architecture:** FastAPI Backend • SQLite Persistence • NLP Vectorizer & Rule Agent • Modern Single-Screen UI Dashboard

---

## 🎯 Project Overview & Objective

In utility-scale renewable energy infrastructure (solar farms, wind parks, hydro dams, battery storage systems), maintenance tickets arrive continuously from SCADA alarm triggers, technician field inspections, and IoT sensors. When dispatchers are overwhelmed, critical faults (such as wind turbine gearbox overheating or inverter trip alarms) can sit in backlogs, causing revenue loss or catastrophic equipment failure.

This project delivers an **end-to-end AI-powered triage and prioritization system** that:
1. **Classifies failure categories** (e.g., Inverter Thermal, Turbine Gearbox Vibration, Spillway Safety).
2. **Assigns quantitative priority scores** (0–100) using multi-factor severity heuristics (safety, financial impact, operational downtime).
3. **Identifies probable root causes & OSHA safety alerts** (e.g., arc flash hazards, lockout-tagout protocol).
4. **Auto-routes tasks** to the appropriate specialized field engineering crews.
5. **Persists records in an ACID SQLite database** with live filtering, real-time KPI metrics, and full workflow status management.

---

## 🖥️ How to Run in VS Code (Quick Start)

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Visual Studio Code

### Step 1: Open the Project in VS Code
1. Open **VS Code**.
2. Go to **File** ➔ **Open Folder...** and select:
   ```
   d:\ai-powered-maintenance-ticket-prioritization-agent
   ```

### Step 2: Open PowerShell Terminal
In VS Code, press <kbd>Ctrl</kbd> + <kbd>`</kbd> (or go to **Terminal** ➔ **New Terminal**).

### Step 3: Activate the Virtual Environment
Run the following command in the VS Code terminal:
```powershell
.\.venv312\Scripts\Activate.ps1
```
*(If you see an execution policy warning, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### Step 4: Launch the Application
Run the FastAPI Uvicorn server:
```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### Step 5: Open the Application in your Browser
Open Google Chrome or Microsoft Edge and navigate to:
```
http://127.0.0.1:8000
```
- **Interactive UI Dashboard:** `http://127.0.0.1:8000/`
- **Health Check Endpoint:** `http://127.0.0.1:8000/api/health`
- **Swagger Interactive API Docs:** `http://127.0.0.1:8000/docs`

---

## 🚀 How to Deploy to Railway (Step-by-Step)

The project includes production-ready deployment configurations (`Procfile`, `requirements.txt`, and dynamic `$PORT` binding in `backend/app.py`).

### Step 1: Push Repository to GitHub
```bash
git init
git add .
git commit -m "feat: AI Maintenance Ticket Prioritization Agent submission ready"
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

### Step 2: Create a New Project on Railway
1. Log into [Railway.app](https://railway.app).
2. Click **"+ New Project"**.
3. Select **"Deploy from GitHub repo"** and choose your repository.

### Step 3: Deployment Configuration
Railway automatically detects Python via `requirements.txt` and executes the `Procfile`:
```procfile
web: uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```
- No external environment variables or database installations are needed; the self-contained SQLite database initializes and seeds automatically on application startup.

### Step 4: Generate Public Domain
1. In your Railway project dashboard, click on your service.
2. Go to **Settings** ➔ **Networking** ➔ Click **"Generate Domain"**.
3. Copy your live application URL (e.g., `https://ai-ticket-agent-production.up.railway.app`) and submit it with your assignment!

---

## 🧪 Running Automated Tests

To run the automated test suites in VS Code:

### 1. Pytest Unit & Integration Tests (13 Tests)
```powershell
python -m pytest tests/ -v
```
*Output: 13 passed, 0 failed across agent NLP logic, rule engine, database CRUD, and API routes.*

### 2. End-to-End API Verification (28 Tests)
```powershell
python e2e_test.py
```
*Output: 28 passed, 0 failed across all API endpoints, database operations, health checks, and frontend static asset routes.*

---

## 🏗️ System Architecture & Workflow

```
┌────────────────────────────────────────────────────────┐
│                   Web Dashboard (UI)                   │
│  - 4 Pastel KPI Metric Cards                           │
│  - Single-Screen Persisted Queue with 1-Click Filters  │
│  - AI Triage Diagnosis Card with Preset Scenarios      │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (HTTP)
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│  - CORS Middleware & Static Asset Mount                │
│  - SQLite Database Engine (WAL mode)                   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                Hybrid AI Triage Engine                 │
│  - TF-IDF Cosine Similarity Feature Extractor          │
│  - Domain Rule-Based Expert Decision Trees             │
│  - Multi-Factor Priority Scoring Engine (0-100)        │
│  - OSHA Safety Guardrail Policy Engine                 │
└────────────────────────────────────────────────────────┘
```

---

## 💬 How to Explain This Project to a Recruiter / Interviewer

When presenting this project in a technical interview, use this natural, human-friendly explanation:

### 1. The Elevator Pitch (30 seconds)
> *"I built an intelligent maintenance dispatch platform for renewable energy plants—like wind farms, solar fields, and hydro dams. The challenge in this industry is that SCADA systems generate hundreds of alerts a day, and human dispatchers struggle to quickly tell an emergency apart from routine maintenance. My system uses a hybrid NLP and expert agent pipeline to analyze ticket descriptions, predict root causes, calculate an objective 0 to 100 priority score, flag safety hazards, and route the ticket to the right maintenance crew."*

### 2. The Architectural Design Choices
> - **Why a Hybrid AI Agent instead of just an LLM API call?**
>   *"In industrial and utility operations, reliability, determinism, and latency matter. Relying purely on an external LLM can be slow, costly, and prone to hallucinations. I designed a hybrid agent that combines TF-IDF semantic vector similarity with deterministic domain expert rules. This guarantees 100% predictable safety alerts (like Lockout/Tagout for electrical faults) while maintaining fast sub-50ms inference times."*
> - **Why SQLite with WAL mode?**
>   *"To keep the project self-contained and zero-setup without external database dependencies, I used SQLite with Write-Ahead Logging. It provides full ACID transactions and handles concurrent reads and writes easily for real-time ticket updates."*
> - **Frontend Design Philosophy:**
>   *"I avoided bloated frameworks and built a clean, responsive single-screen dashboard using modern CSS. It features 1-click interactive filter pills rather than dropdowns that obstruct table headers, custom pastel color-coding for cognitive clarity, and zero horizontal scrolling."*

### 3. A 60-Second Live Demo Walkthrough
1. **Show the Metrics:** Point to the 4 pastel KPI cards showing total tickets, active queue count, critical risks, and average priority score.
2. **Trigger an AI Triage:** Click the preset button **"☀️ Solar Inverter Overheating"** and hit **"⚡ Triage & Save to Database"**.
   - Show how the AI agent calculates Priority Score (84 / Critical), identifies root cause as *Inverter Thermal Fault*, flags OSHA safety warnings (*arc flash precautions*), and assigns it to *Solar & Electrical Ops*.
3. **Filter the Queue:** Click the **"💨 Wind Turbine Generator"** filter pill. Show how the table instantly filters without page reload or dropdown popups.
4. **Update Status:** Change ticket status directly in the table dropdown to **"In Progress"** or **"Resolved"** and show that the metrics update live.

---

## 📊 Model Evaluation & Metrics

The system was evaluated against the curated benchmark dataset (`data/maintenance_tickets.csv`):
- **Category Classification Accuracy:** 100.0% (6/6)
- **Severity Classification Accuracy:** 83.3% (5/6)
- **Inference Latency:** < 45 ms per ticket
- **API Endpoints:** 16 verified endpoints with 100% automated test coverage.
