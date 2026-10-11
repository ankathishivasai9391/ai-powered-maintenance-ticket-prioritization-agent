# 🛠️ VS Code Developer Guide — Professional Setup & Rules

<p align="center">
  <img src="https://img.shields.io/badge/VS_Code-Setup_Guide-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

<p align="center">
  <strong>Complete professional development environment setup for the AI-Powered Maintenance Ticket Prioritization Agent</strong>
</p>

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Step 1 — Clone & Open in VS Code](#-step-1--clone--open-in-vs-code)
- [Step 2 — Python Environment Setup](#-step-2--python-environment-setup)
- [Step 3 — Install Dependencies](#-step-3--install-dependencies)
- [Step 4 — VS Code Configuration (Auto-Applied)](#-step-4--vs-code-configuration-auto-applied)
- [Step 5 — Install Recommended Extensions](#-step-5--install-recommended-extensions)
- [Step 6 — Run the Dev Server](#-step-6--run-the-dev-server)
- [Step 7 — Run Tests](#-step-7--run-tests)
- [Step 8 — End-to-End API Testing](#-step-8--end-to-end-api-testing)
- [Step 9 — Docker Build & Run](#-step-9--docker-build--run)
- [Step 10 — Deploy to Railway](#-step-10--deploy-to-railway)
- [VS Code Keyboard Shortcuts](#-vs-code-keyboard-shortcuts)
- [Project Architecture Reference](#-project-architecture-reference)
- [Troubleshooting](#-troubleshooting)

---

## 📦 Prerequisites

Before starting, ensure you have the following installed:

| Tool | Version | Download |
|:---|:---|:---|
| **VS Code** | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Python** | 3.12+ | [python.org/downloads](https://www.python.org/downloads/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |
| **Docker** *(optional)* | Latest | [docker.com](https://www.docker.com/) |

> **✅ Verify Installation:**
> ```powershell
> python --version    # → Python 3.12.x
> git --version       # → git version 2.x.x
> code --version      # → 1.x.x
> docker --version    # → Docker version 2x.x (optional)
> ```

---

## 🚀 Step 1 — Clone & Open in VS Code

### Option A: Command Line
```powershell
# Clone the repository
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git

# Open in VS Code
code ai-powered-maintenance-ticket-prioritization-agent
```

### Option B: VS Code GUI
1. Open VS Code
2. Press `Ctrl + Shift + P` → type **"Git: Clone"**
3. Paste: `https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git`
4. Choose a local folder → Click **"Open"**

---

## 🐍 Step 2 — Python Environment Setup

### Create Virtual Environment

**Windows (PowerShell):**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Select Python Interpreter in VS Code

1. Press `Ctrl + Shift + P`
2. Type: **"Python: Select Interpreter"**
3. Choose: `.venv` → `Python 3.12.x`

> 💡 The `.vscode/settings.json` already points to the correct interpreter — VS Code should auto-detect it.

---

## 📥 Step 3 — Install Dependencies

Open the **VS Code Integrated Terminal** (`Ctrl + `` ` ``):

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Or use the VS Code Task:**
- Press `Ctrl + Shift + P` → **"Tasks: Run Task"** → **"📦 Install Dependencies"**

### Installed Packages

| Package | Purpose |
|:---|:---|
| `fastapi==0.115.0` | High-performance async web framework |
| `uvicorn==0.30.6` | ASGI server for FastAPI |
| `numpy==1.26.4` | Numerical computation for TF-IDF |
| `scikit-learn==1.5.1` | TF-IDF Vectorizer + Cosine Similarity |
| `pydantic==2.8.2` | Data validation and serialization |
| `python-multipart==0.0.9` | Form data parsing support |
| `httpx==0.28.1` | Async HTTP client for testing |

---

## ⚙️ Step 4 — VS Code Configuration (Auto-Applied)

The project includes a complete `.vscode/` setup that auto-activates when you open the folder:

### 📁 `.vscode/settings.json`
| Setting | Purpose |
|:---|:---|
| Python interpreter path | Points to `.venv312` |
| Format on save | Auto-formats Python, HTML, JSON |
| pytest integration | One-click test discovery & execution |
| File exclusions | Hides `__pycache__`, `.pytest_cache`, `.venv` |
| Terminal PYTHONPATH | Ensures module imports work in terminal |
| Trailing whitespace trim | Clean code on every save |

### 📁 `.vscode/launch.json` — Debug Configurations

| Configuration | What It Does |
|:---|:---|
| 🚀 **FastAPI Server (Dev)** | Starts uvicorn with `--reload` for hot-reloading |
| 🧪 **Run All Tests** | Runs `pytest tests/ -v` with debugger attached |
| 🌐 **E2E API Test** | Runs `e2e_test.py` (28 endpoint checks) |
| 📊 **Run Evaluation** | Starts server for benchmark evaluation |
| 🔥 **Full Stack Debug** | Compound: starts server with full debugging |

**How to use:**
1. Press `F5` or click the **Run and Debug** sidebar (`Ctrl + Shift + D`)
2. Select a configuration from the dropdown
3. Click the ▶️ **Play** button

### 📁 `.vscode/tasks.json` — Quick Tasks

| Task | Shortcut |
|:---|:---|
| 🚀 Start Dev Server | `Ctrl+Shift+P` → Tasks → Select |
| 🧪 Run All Tests | `Ctrl+Shift+P` → Tasks → Select |
| 🌐 Run E2E Tests | `Ctrl+Shift+P` → Tasks → Select |
| 📦 Install Dependencies | `Ctrl+Shift+P` → Tasks → Select |
| 🐳 Docker Build | `Ctrl+Shift+P` → Tasks → Select |
| 🐳 Docker Run | `Ctrl+Shift+P` → Tasks → Select |
| 🔄 Git Push to Deploy | `Ctrl+Shift+P` → Tasks → Select |

### 📁 `.vscode/extensions.json` — Recommended Extensions

Auto-prompted when you open the project. Install all for the best experience.

---

## 🔌 Step 5 — Install Recommended Extensions

When you open the project, VS Code shows a popup:
> *"This workspace has extension recommendations. Would you like to install them?"*

Click **"Install All"**. Or install manually:

| Extension | Purpose |
|:---|:---|
| 🐍 **Python** (`ms-python.python`) | Core Python language support |
| 🐛 **Debugpy** (`ms-python.debugpy`) | Python debugging |
| 🧠 **Pylance** (`ms-python.vscode-pylance`) | IntelliSense, type checking, auto-imports |
| 🌐 **Live Server** (`ritwickdey.LiveServer`) | Preview frontend HTML live |
| 🔗 **REST Client** (`humao.rest-client`) | Test API endpoints from `.http` files |
| 🐳 **Docker** (`ms-azuretools.vscode-docker`) | Dockerfile syntax, build, run |
| ✨ **Prettier** (`esbenp.prettier-vscode`) | HTML/JSON/CSS formatting |
| 📜 **GitLens** (`eamodio.gitlens`) | Advanced Git blame, history, diffs |
| 📝 **Markdown All in One** (`yzhang.markdown-all-in-one`) | TOC, preview, shortcuts |
| ✏️ **Code Spell Checker** (`streetsidesoftware.code-spell-checker`) | Catch typos in code & docs |

---

## ▶️ Step 6 — Run the Dev Server

### Method 1: VS Code Debug (Recommended)
1. Press `F5`
2. Select **"🚀 FastAPI Server (Dev)"**
3. Server starts at `http://127.0.0.1:8000` with hot-reload

### Method 2: Terminal
```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### Method 3: VS Code Task
- `Ctrl + Shift + P` → **"Tasks: Run Task"** → **"🚀 Start Dev Server"**

### 🌐 Open in Browser

| Resource | URL |
|:---|:---|
| 🖥️ **Dashboard** | http://127.0.0.1:8000/ |
| 📖 **Swagger UI** | http://127.0.0.1:8000/docs |
| ❤️ **Health Check** | http://127.0.0.1:8000/api/health |
| 📊 **API Metrics** | http://127.0.0.1:8000/api/metrics |

> 💡 **Tip:** Click **"Reset / Seed Benchmark Dataset"** in the dashboard header to pre-load sample tickets.

---

## 🧪 Step 7 — Run Tests

### Method 1: VS Code Test Explorer (Best)
1. Click the 🧪 **Testing** icon in the sidebar
2. VS Code auto-discovers all tests in `tests/`
3. Click ▶️ to run all, or click individual tests

### Method 2: Debug Tests
1. Press `Ctrl + Shift + D`
2. Select **"🧪 Run All Tests"**
3. Press `F5` — tests run with full debugger (set breakpoints!)

### Method 3: Terminal
```powershell
python -m pytest tests/ -v --tb=short
```

### Expected Output
```
tests/test_agent.py::test_predict_category_inverter       PASSED
tests/test_agent.py::test_predict_category_gearbox         PASSED
tests/test_agent.py::test_determine_severity_critical      PASSED
tests/test_agent.py::test_rag_find_similar_tickets         PASSED
tests/test_agent.py::test_evaluate_benchmark               PASSED
tests/test_api.py::test_demo_endpoint                      PASSED
tests/test_api.py::test_run_endpoint                       PASSED
tests/test_api.py::test_analyze_endpoint                   PASSED
tests/test_api.py::test_create_and_manage_ticket_endpoint  PASSED
tests/test_api.py::test_metrics_endpoint                   PASSED
tests/test_api.py::test_evaluation_endpoint                PASSED
tests/test_api.py::test_health_endpoint                    PASSED
tests/test_database.py::test_database_crud_flow            PASSED

======================== 13 passed ========================
```

---

## 🌐 Step 8 — End-to-End API Testing

The E2E test validates all 17 API scenarios (28 assertions) against a live server:

### Run E2E Test
```powershell
# Terminal 1: Start server
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000

# Terminal 2: Run E2E tests
python e2e_test.py
```

### Expected Output
```
============================================================
END-TO-END API TEST
============================================================

[1]  GET /api/demo           → PASS
[2]  POST /api/run            → PASS (3 checks)
[3]  POST /api/analyze        → PASS (severity, priority, team)
[4]  GET /api/tickets          → PASS (seeded tickets exist)
[5]  POST /api/tickets         → PASS (create)
[6]  GET /api/tickets/{id}     → PASS (retrieve)
[7]  PATCH status              → PASS (in_progress)
[8]  PATCH assign              → PASS (team updated)
[9]  Filter: asset_type=wind   → PASS
[10] Filter: severity=critical → PASS
[11] Filter: status=in_progress→ PASS
[12] GET /api/metrics          → PASS (4 metric fields)
[13] GET /api/evaluation       → PASS (benchmark)
[14] DELETE /api/tickets/{id}  → PASS
[15] GET deleted (404)         → PASS
[16] GET / (frontend HTML)     → PASS
[17] GET /api/health           → PASS

============================================================
RESULTS: 28 passed, 0 failed, 28 total
============================================================
```

---

## 🐳 Step 9 — Docker Build & Run

### VS Code Task (One-Click)
- `Ctrl + Shift + P` → **"Tasks: Run Task"** → **"🐳 Docker Build"**
- Then → **"🐳 Docker Run"**

### Terminal
```powershell
# Build the Docker image
docker build -t ticket-agent .

# Run the container
docker run -p 8000:8000 -e PORT=8000 ticket-agent

# Open: http://localhost:8000
```

### Dockerfile Summary
```dockerfile
FROM python:3.12-slim
# → Installs libgomp1 (required by scikit-learn)
# → Installs Python dependencies
# → Copies project files
# → Runs: python backend/app.py
```

---

## 🚀 Step 10 — Deploy to Railway

### Automatic Deployment (CI/CD)
Railway auto-deploys on every `git push` to `main`:

```powershell
git add .
git commit -m "feat: your changes"
git push origin main
# → Railway auto-builds from Dockerfile & deploys
```

### Or use the VS Code Task:
- `Ctrl + Shift + P` → **"Tasks: Run Task"** → **"🔄 Git Push to Deploy"**

### Manual Railway Setup (First Time)
1. Go to [railway.app](https://railway.app) → **New Project**
2. Select **"Deploy from GitHub repo"**
3. Choose: `ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent`
4. Railway auto-detects the `Dockerfile` builder
5. Environment variable `PORT` is auto-injected
6. Click **Deploy** → Live URL generated

### Deployment Configuration Files

| File | Purpose |
|:---|:---|
| `Dockerfile` | Container build (python:3.12-slim + libgomp1) |
| `railway.json` | Railway builder config (Dockerfile mode) |
| `Procfile` | Process declaration: `web: python backend/app.py` |
| `nixpacks.toml` | Nixpacks apt dependency: `libgomp1` |
| `.python-version` | Pin Python 3.12.8 for cloud builders |

### Live Deployment URLs

| Resource | URL |
|:---|:---|
| 🌐 Dashboard | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/ |
| 📖 Swagger | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/docs |
| ❤️ Health | https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/health |

---

## ⌨️ VS Code Keyboard Shortcuts

| Action | Shortcut |
|:---|:---|
| **Start Debugging** | `F5` |
| **Stop Debugging** | `Shift + F5` |
| **Restart Debugging** | `Ctrl + Shift + F5` |
| **Toggle Breakpoint** | `F9` |
| **Open Terminal** | `` Ctrl + ` `` |
| **Run Task** | `Ctrl + Shift + P` → "Tasks: Run Task" |
| **Select Python Interpreter** | `Ctrl + Shift + P` → "Python: Select Interpreter" |
| **Run Test at Cursor** | `Ctrl + Shift + P` → "Python: Run Test at Cursor" |
| **Open Test Explorer** | Click 🧪 icon in sidebar |
| **Git Commit** | `Ctrl + Shift + G` → type message → `Ctrl + Enter` |
| **Toggle Sidebar** | `Ctrl + B` |
| **Quick Open File** | `Ctrl + P` |
| **Search Across Files** | `Ctrl + Shift + F` |
| **Format Document** | `Shift + Alt + F` |
| **Go to Definition** | `F12` |
| **Peek Definition** | `Alt + F12` |

---

## 🏗️ Project Architecture Reference

```
ai-powered-maintenance-ticket-prioritization-agent/
│
├── .vscode/                          ← VS Code workspace config
│   ├── settings.json                 ← Editor, Python, testing, exclusions
│   ├── launch.json                   ← Debug configurations (F5)
│   ├── tasks.json                    ← Build & test tasks
│   └── extensions.json               ← Recommended extensions
│
├── backend/
│   ├── app.py                        ← FastAPI application + routes
│   ├── agent.py                      ← AI agent: TF-IDF + rules + scoring
│   ├── database.py                   ← SQLite CRUD operations
│   ├── schemas.py                    ← Pydantic models (request/response)
│   ├── config.py                     ← Paths and environment config
│   └── data/
│       └── dataset_loader.py         ← CSV benchmark data loader
│
├── frontend/
│   └── index.html                    ← Single-page dashboard (HTML+CSS+JS)
│
├── tests/
│   ├── test_agent.py                 ← AI agent unit tests (5 tests)
│   ├── test_api.py                   ← API integration tests (7 tests)
│   └── test_database.py              ← Database CRUD tests (1 test)
│
├── data/
│   └── maintenance_tickets.csv       ← 6-sample labeled benchmark dataset
│
├── docs/
│   ├── ARCHITECTURE.md               ← System design decisions
│   └── API_EXAMPLES.md               ← cURL + Python API examples
│
├── e2e_test.py                       ← End-to-end live API test (28 checks)
├── requirements.txt                  ← Python dependencies (pinned)
├── Dockerfile                        ← Docker container spec
├── railway.json                      ← Railway deployment config
├── Procfile                          ← PaaS process file
├── nixpacks.toml                     ← Nixpacks apt dependency
├── .python-version                   ← Python version pin (3.12.8)
├── .env.example                      ← Environment variable template
├── .gitignore                        ← Git exclusions
├── EVALUATION.md                     ← Benchmark methodology & results
├── DEMO_NOTES.md                     ← Quick reviewer demo guide
└── LIMITATIONS_AND_ROADMAP.md        ← Constraints & future plans
```

---

## 🔧 Troubleshooting

### ❌ "Module not found" errors
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Ensure PYTHONPATH is set
$env:PYTHONPATH = "."

# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ "uvicorn not recognized"
```powershell
# Use python module syntax instead
python -m uvicorn backend.app:app --reload
```

### ❌ Tests fail with DB errors
```powershell
# Tests use isolated temp databases — won't affect production
# If issues persist, delete and reinitialize:
Remove-Item data/maintenance.db -ErrorAction SilentlyContinue
python -m uvicorn backend.app:app  # auto-recreates DB on startup
```

### ❌ Port 8000 already in use
```powershell
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
python -m uvicorn backend.app:app --port 8001
```

### ❌ numpy/scikit-learn won't install (Python 3.14+)
```powershell
# Use Python 3.12 which has pre-built wheels
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ Docker build fails
```powershell
# Ensure Docker Desktop is running
docker info

# Clean and rebuild
docker system prune -f
docker build --no-cache -t ticket-agent .
```

---

## 📊 Quick Verification Checklist

Run through this checklist to confirm everything works:

- [ ] ✅ Python 3.12 virtual environment activated
- [ ] ✅ All dependencies installed (`pip install -r requirements.txt`)
- [ ] ✅ VS Code shows correct Python interpreter (bottom-left status bar)
- [ ] ✅ `F5` → FastAPI server starts with hot-reload
- [ ] ✅ Dashboard loads at http://127.0.0.1:8000/
- [ ] ✅ Swagger UI loads at http://127.0.0.1:8000/docs
- [ ] ✅ Health check returns `"healthy"` at /api/health
- [ ] ✅ `pytest tests/ -v` → 13/13 tests pass
- [ ] ✅ `python e2e_test.py` → 28/28 checks pass
- [ ] ✅ `git push origin main` → Railway auto-deploys

---

<p align="center">
  <strong>🎯 You're all set! Happy coding!</strong><br/>
  Built by <a href="https://github.com/ankathishivasai9391">Shivasai Ankathi</a> · Python · FastAPI · TF-IDF · Railway
</p>
