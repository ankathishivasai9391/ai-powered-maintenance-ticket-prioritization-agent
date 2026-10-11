# AI-Powered Maintenance Ticket Prioritization Agent

A full-stack application designed to organize maintenance requests and prioritize tickets based on their urgency and impact. Built with Python, FastAPI, SQLite, and a web dashboard, the project demonstrates backend API development, data management, testing, and deployment preparation.

**Repository:** [View Source Code on GitHub](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

## Overview

Maintenance teams often handle multiple requests at the same time. Without a consistent prioritization process, urgent issues can be overlooked and response times can increase.

This project provides a centralized application for managing maintenance tickets, reviewing priority classifications, and supporting more organized maintenance workflows.

## Key Features

- **Ticket Prioritization:** Classifies maintenance tickets using the prioritization logic implemented in the application.
- **Maintenance Dashboard:** Provides a web interface for viewing ticket information.
- **REST API:** Exposes backend functionality through FastAPI.
- **SQLite Database:** Stores application data locally.
- **CSV-Based Initialization:** Supports loading initial ticket data when the database is empty, according to the implemented initialization logic.
- **API Documentation:** Provides interactive API documentation through Swagger UI.
- **Automated Testing:** Includes tests to help validate application behavior.
- **Deployment Configuration:** Includes a Procfile for starting the application with Uvicorn.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Existing web dashboard |
| Database | SQLite |
| API Documentation | Swagger UI, OpenAPI |
| Testing | Pytest |
| Server | Uvicorn |
| Version Control | Git, GitHub |

## Architecture

```text
User
  |
  v
Web Dashboard
  |
  v
FastAPI Backend
  |
  +---- Ticket Prioritization Logic
  |
  +---- Ticket Management
  |
  v
SQLite Database
```

## Project Structure

```text
ai-powered-maintenance-ticket-prioritization-agent/
├── backend/
│   └── app.py
├── frontend/
├── data/
│   └── maintenance_tickets.csv
├── tests/
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

*The structure above is representative. Refer to the repository for the complete file listing.*

## Getting Started

### Prerequisites

- Python 3.10 or a version supported by the project dependencies
- Git
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
cd ai-powered-maintenance-ticket-prioritization-agent
```

### 2. Create and activate a virtual environment

**Windows:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

If port `8000` is unavailable, choose another free port.

### 5. Access the application

| Resource | URL |
|---|---|
| Web Dashboard | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Interactive API Docs | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Health Check | [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health) |

Keep the terminal running while using the application.

## API Documentation

The application uses FastAPI to expose backend functionality. Open `/docs` while the server is running to explore the implemented endpoints and try supported requests interactively.

Health-check endpoint:

```http
GET /api/health
```

Consult the interactive API documentation for the actual request formats, response schemas, and available operations.

## Database

The application uses SQLite for local data storage. The database location can be configured through the `DB_PATH` environment variable; otherwise, the application uses its configured default path.

The initialization logic can load initial ticket records from CSV when the database is empty.

For production use, configure persistent storage or a managed database so important records are retained across deployments and restarts.

## Testing

Run the test suite from the project root:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

Run tests after making changes to check that existing functionality continues to work.

## Deployment

The repository includes a `Procfile` for launching the application with Uvicorn.

For a compatible hosting platform, use:

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

Configure environment variables and persistent storage according to the hosting provider. SQLite data stored on an ephemeral filesystem may be lost when the service restarts or is redeployed.

## Future Enhancements

Potential extensions include:

- Machine-learning-based priority prediction.
- Natural-language processing for maintenance descriptions.
- Explainable priority recommendations.
- Advanced filtering, analytics, and reporting.
- Notifications for critical tickets.
- Role-based access control and audit history.
- Integration with external maintenance management systems.

These are proposed enhancements rather than existing features unless implemented in the code.

## Skills Demonstrated

- Python backend development
- REST API design with FastAPI
- Relational data persistence using SQLite
- CSV data processing
- Automated testing
- Git and GitHub workflows
- Application configuration and deployment preparation

## Author

**Shivasai Ankathi**

- GitHub: [ankathishivasai9391](https://github.com/ankathishivasai9391)
- Project: [AI-Powered Maintenance Ticket Prioritization Agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

## License

No open-source license has been specified. Add a `LICENSE` file if you decide to publish the project under a particular license.

---

If this project is useful to you, consider giving the repository a ⭐.
