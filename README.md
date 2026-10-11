# ⚡ AI-Powered Maintenance Ticket Prioritization Agent

<p align="center">
  <strong>Smarter Maintenance. Structured Priorities. Better Workflows.</strong>
  <br />
  A Python-powered application for organizing maintenance tickets and supporting priority-driven decision-making.
</p>

<p align="center">
  <a href="https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent">
    <img src="https://img.shields.io/badge/Project-Maintenance%20AI-6C63FF?style=for-the-badge" alt="Maintenance AI Project" />
  </a>
  <img src="https://img.shields.io/badge/Python-Backend-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</p>

<p align="center">
  <a href="#-overview">Overview</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-architecture">Architecture</a> ·
  <a href="#-getting-started">Getting Started</a> ·
  <a href="#-testing">Testing</a>
</p>

---

## 🎯 Overview

Maintenance teams often receive multiple service requests with different levels of urgency and operational impact. Without a consistent workflow, identifying which issue needs attention first can become challenging.

The **AI-Powered Maintenance Ticket Prioritization Agent** is a full-stack application designed to organize maintenance-ticket information, apply the prioritization logic implemented in the application, and provide a web interface for reviewing ticket data.

The project demonstrates practical software engineering concepts, including API development, database integration, structured data processing, automated testing, and deployment preparation.

## 💎 Why This Project?

- **Problem-focused:** Addresses the challenge of organizing and evaluating maintenance requests.
- **API-driven:** Uses FastAPI to expose backend functionality.
- **Data-oriented:** Works with structured ticket data and SQLite persistence.
- **Developer-friendly:** Includes interactive API documentation and local setup instructions.
- **Extensible:** Provides a foundation for future predictive analytics and machine-learning capabilities.

## ✨ Features

| Feature | Description |
|---|---|
| 🎫 Ticket prioritization | Applies the priority logic implemented in the application |
| 🖥️ Web dashboard | Presents maintenance information through a browser interface |
| 🔌 REST API | Provides backend operations through FastAPI |
| 🗄️ SQLite storage | Supports local data persistence |
| 📄 CSV initialization | Supports initial data loading when configured and applicable |
| 📚 Interactive API docs | Allows exploration of API endpoints using Swagger UI |
| 🧪 Automated testing | Supports verification of application behavior |
| ☁️ Deployment configuration | Includes a Uvicorn startup configuration for compatible hosting |

## 🖼️ Application Preview

Add a screenshot of your actual running dashboard to the repository at `docs/images/dashboard.png`.

Then display it here:

<p align="center">
  <img src="docs/images/dashboard.png" alt="Maintenance Ticket Dashboard" width="900" />
</p>

> Replace this placeholder with a genuine screenshot before publishing the README. If you do not have a screenshot yet, remove this section until one is available.

## 🏗️ Architecture

```text
                     USER
                       |
                       v
                WEB DASHBOARD
                       |
                       v
                 FASTAPI BACKEND
                       |
             +---------+---------+
             |                   |
             v                   v
       PRIORITY LOGIC       API OPERATIONS
             |                   |
             +---------+---------+
                       |
                       v
                 SQLITE DATABASE
```

### Application workflow

1. A user accesses the web dashboard.
2. The frontend communicates with backend endpoints where required.
3. FastAPI processes supported requests.
4. The application applies its implemented ticket-management and prioritization logic.
5. Data is read from or written to the configured database.
6. The API returns the appropriate response.

The exact workflow depends on the implemented endpoint and operation.

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend framework | FastAPI |
| Application server | Uvicorn |
| Database | SQLite |
| Initial data format | CSV |
| API documentation | OpenAPI / Swagger UI |
| Testing framework | Pytest |
| Version control | Git and GitHub |
| Development environment | Visual Studio Code |

## 📁 Project Structure

```text
ai-powered-maintenance-ticket-prioritization-agent/
│
├── backend/
│   └── app.py
│
├── frontend/
├── data/
├── tests/
│
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

This is a simplified overview. See the repository for the complete source code and actual file structure.

## 🚀 Getting Started

### Prerequisites

Install the following before running the application:

- Python version compatible with `requirements.txt`
- Git
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
```

### 2. Navigate to the project directory

```bash
cd ai-powered-maintenance-ticket-prioritization-agent
```

### 3. Create a virtual environment

**Windows**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the backend

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

If port `8000` is occupied, choose another available port.

### 6. Open the application

| Resource | URL |
|---|---|
| Dashboard | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Swagger UI | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Health check | [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health) |

Keep the terminal running while using the application.

## 🔌 API Documentation

FastAPI generates interactive API documentation for the application's implemented endpoints.

Open `/docs` to:

- Explore available routes.
- Inspect request and response schemas.
- Submit supported test requests.
- Understand the backend API contract.

The application includes a health-check route:

```http
GET /api/health
```

Refer to the running documentation for the complete endpoint list and expected responses.

## 🗄️ Database and Data Initialization

The application uses SQLite for local persistence.

The database path can be configured through the `DB_PATH` environment variable. Otherwise, the application uses its configured default path.

According to the initialization logic, CSV data can be used to populate an empty database.

For production deployment, configure persistent storage or a managed database if records must survive restarts and redeployments.

## 🧪 Testing

Run the tests from the project root:

```bash
python -m pytest
```

For detailed output:

```bash
python -m pytest -v
```

Run the tests after making changes to help detect regressions and verify expected behavior.

## ☁️ Deployment

The repository includes a `Procfile` for launching the FastAPI application with Uvicorn.

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

Configure these commands according to your hosting provider.

### Production considerations

- Configure persistent database storage.
- Keep credentials and secrets out of source control.
- Validate incoming requests and handle errors consistently.
- Use HTTPS and appropriate access controls.
- Monitor application errors and service health.
- Verify the application and its dependencies before deployment.

## 🔭 Future Enhancements

Potential improvements for future versions include:

- Machine-learning-based priority prediction.
- Natural-language processing for maintenance descriptions.
- Explainable priority recommendations.
- Advanced ticket filtering and analytics.
- Notifications for critical maintenance issues.
- Role-based access control and audit history.
- Integration with external maintenance-management systems.
- Managed database support for production deployments.

These are proposed enhancements and should not be presented as existing functionality unless implemented.

## 🧠 Engineering Skills Demonstrated

- Python backend development.
- REST API design using FastAPI.
- SQLite database integration.
- Structured data processing.
- Automated testing with Pytest.
- Git and GitHub workflows.
- Environment configuration.
- Application deployment preparation.

## 👨‍💻 Author

**Shivasai Ankathi**

- GitHub Profile: [ankathishivasai9391](https://github.com/ankathishivasai9391)
- Project Repository: [AI-Powered Maintenance Ticket Prioritization Agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

---

<p align="center">
  <strong>Built with Python. Designed around practical maintenance workflows.</strong>
  <br />
  If you find this project useful, consider giving the repository a ⭐.
</p>


