# 🚀 AI-Powered Maintenance Ticket Prioritization Agent

A full-stack application for managing maintenance tickets and identifying issues that need attention first. This project combines a Python backend, a web dashboard, and SQLite database storage to provide a structured maintenance-ticket workflow.

## 📌 Project Overview

Maintenance teams often receive multiple requests, but not every issue has the same level of urgency.

This application helps organize maintenance tickets and prioritize them using the prioritization logic implemented in the system. It provides a centralized dashboard and backend APIs for working with maintenance data.

## ✨ Features

- **Ticket Prioritization:** Classifies maintenance tickets using the application's implemented prioritization rules.
- **Web Dashboard:** Provides an interface for viewing maintenance-ticket information.
- **FastAPI Backend:** Exposes application functionality through REST APIs.
- **SQLite Database:** Stores maintenance data locally.
- **CSV Data Initialization:** Supports loading initial ticket data when the database is empty.
- **Interactive API Documentation:** Explore available endpoints using Swagger UI.
- **Automated Testing:** Includes tests for validating application behavior.
- **Deployment Ready:** Includes a Procfile for starting the application with Uvicorn.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Web dashboard
- **Database:** SQLite
- **API Documentation:** Swagger UI, OpenAPI
- **Testing:** Pytest
- **Server:** Uvicorn
- **Tools:** Visual Studio Code, Git, GitHub

## 🏗️ Application Architecture

```text
          User
           |
           v
     Web Dashboard
           |
           v
      FastAPI Backend
           |
     +-----+------+
     |            |
     v            v
Ticket Logic   API Operations
     |            |
     +-----+------+
           |
           v
      SQLite Database
```

## 📂 Project Structure

```text
ai-powered-maintenance-ticket-prioritization-agent/
│
├── backend/
│   └── app.py
├── frontend/
├── data/
├── tests/
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

Refer to the repository for the complete project structure.

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your system
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
```

### Step 2: Open the Project Folder

```bash
cd ai-powered-maintenance-ticket-prioritization-agent
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

If port `8000` is unavailable, use another available port.

## 🌐 Application URLs

Once the server starts, open these URLs in your browser.

| Resource | URL |
|---|---|
| Web Dashboard | http://127.0.0.1:8000/ |
| API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/api/health |

## 🔌 API Documentation

The application uses FastAPI to provide backend API functionality.

Open `/docs` to explore the implemented endpoints, view request and response schemas, and test supported operations.

Health-check endpoint:

`GET /api/health`

## 🗄️ Database Management

SQLite is used for local data persistence. The database location can be configured using the `DB_PATH` environment variable.

The application supports initializing the database with CSV data when the database contains no records, according to the existing implementation.

For production deployment, configure persistent storage or a managed database to protect data across restarts and redeployments.

## 🧪 Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest
```

For detailed test output:

```bash
python -m pytest -v
```

## ☁️ Deployment

The project includes a `Procfile` for starting the FastAPI application with Uvicorn.

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

Set the commands in your hosting provider's configuration. Configure persistent database storage before using the application for important production records.

## 🔮 Future Enhancements

- Machine-learning-based ticket priority prediction.
- Natural-language processing for maintenance descriptions.
- Explainable priority recommendations.
- Advanced ticket search and filtering.
- Maintenance analytics and reporting.
- Notifications for critical issues.
- Role-based access control.
- Integration with external maintenance systems.

These are potential future improvements, not features claimed to be implemented already.

## 🎓 What I Learned

Through this project, I gained practical experience with:

- Developing backend APIs using Python and FastAPI.
- Working with SQLite and structured data.
- Organizing application logic.
- Testing application functionality.
- Managing source code using Git and GitHub.
- Preparing a web application for deployment.

## 👨‍💻 Author

**Shivasai Ankathi**

GitHub: [ankathishivasai9391](https://github.com/ankathishivasai9391)

**Project Repository:** [AI-Powered Maintenance Ticket Prioritization Agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

---

⭐ If you find this project interesting, consider starring the repository.

