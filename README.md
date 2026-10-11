# AI-Powered Maintenance Ticket Prioritization Agent

An AI-assisted maintenance ticket management application that classifies
incoming maintenance requests, estimates severity and priority, and
recommends the team best suited to handle each ticket. It includes a web
dashboard, REST API, evaluation metrics, and a lightweight
database-backed workflow.

```{=html}
<p align="center">
```
`<strong>`{=html}FastAPI · Python · TF-IDF Similarity · Hybrid
Rule-Based Reasoning · SQLite · HTML/CSS/JavaScript ·
Railway`</strong>`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<a href="https://web-production-18808.up.railway.app/">`{=html}Live
Dashboard`</a>`{=html} ·
`<a href="https://web-production-18808.up.railway.app/docs">`{=html}API
Documentation`</a>`{=html} ·
`<a href="https://web-production-18808.up.railway.app/api/health">`{=html}Health
Check`</a>`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Key Features](#key-features)
-   [How It Works](#how-it-works)
-   [Technology Stack](#technology-stack)
-   [Project Structure](#project-structure)
-   [Run Locally in VS Code](#run-locally-in-vs-code)
-   [Configuration](#configuration)
-   [API Endpoints](#api-endpoints)
-   [Evaluation](#evaluation)
-   [Testing](#testing)
-   [Railway Deployment](#railway-deployment)
-   [Troubleshooting](#troubleshooting)
-   [Limitations and Responsible Use](#limitations-and-responsible-use)
-   [Future Improvements](#future-improvements)

## Overview

Maintenance teams receive requests involving equipment failures,
inspections, electrical issues, HVAC problems, and other facility
concerns. Manually reviewing and routing every request can delay work
and lead to inconsistent prioritization.

This project provides an AI-assisted workflow that takes a maintenance
ticket as input and returns structured prioritization information, such
as:

-   Predicted maintenance category
-   Estimated severity
-   Priority score
-   Recommended maintenance team
-   API-backed ticket and dashboard information

The application is designed as a practical full-stack assessment
project. It combines a Python backend, a browser-based dashboard,
similarity-based text matching, rule-based decision logic, and
persistent ticket storage.

> **Important:** The system provides decision support. A qualified
> maintenance professional should review safety-critical recommendations
> before acting on them.

## Key Features

-   **Ticket analysis:** Analyze maintenance descriptions and return
    structured results.
-   **Category prediction:** Match a ticket against known maintenance
    categories.
-   **Severity estimation:** Apply the application's hybrid analysis
    logic to estimate urgency.
-   **Priority scoring:** Produce a numeric priority score to help sort
    incoming requests.
-   **Team recommendation:** Suggest a maintenance team based on the
    ticket details.
-   **Web dashboard:** View and interact with the application through a
    browser.
-   **REST API:** Access the backend through documented HTTP endpoints.
-   **Evaluation panel:** Display benchmark category and severity
    results.
-   **Database integration:** Store ticket data using SQLite.
-   **Similarity fallback:** The project includes a pure-Python
    similarity fallback if the optional scikit-learn import is
    unavailable, according to the implemented fallback logic.
-   **Automated tests:** Includes unit/integration tests and an
    end-to-end API test script.

## How It Works

``` text
User submits a maintenance request
                |
                v
        FastAPI backend
                |
                v
      Input processing and analysis
                |
                v
 TF-IDF similarity + hybrid rule-based logic
                |
                v
 Category, severity, priority score,
 and recommended maintenance team
                |
       +--------+--------+
       |                 |
       v                 v
  Web dashboard     SQLite database
       |
       v
 User reviews the recommendation
```

The similarity component compares ticket text with known examples or
category descriptions. The hybrid rule-based logic applies the project's
maintenance rules to help determine the resulting classification and
priority. The exact result depends on the input, available reference
data, and rules implemented in the repository.

## Technology Stack

  -----------------------------------------------------------------------
  Area                                Technologies
  ----------------------------------- -----------------------------------
  Backend                             Python, FastAPI, Uvicorn

  API documentation                   OpenAPI / Swagger UI

  Text analysis                       TF-IDF and cosine similarity, with
                                      a pure-Python fallback

  Decision logic                      Hybrid rule-based maintenance
                                      analysis

  Frontend                            HTML, CSS, JavaScript

  Database                            SQLite

  Testing                             pytest and an end-to-end API test
                                      script

  Deployment                          Docker and Railway
  -----------------------------------------------------------------------

## Project Structure

The repository includes the following main components. Some filenames
may differ if you have made further changes.

``` text
ai-powered-maintenance-ticket-prioritization-agent/
├── backend/
│   ├── app.py              # FastAPI application and API routes
│   └── agent.py            # Ticket analysis and prioritization logic
├── frontend/
│   └── index.html          # Browser dashboard
├── tests/                  # Unit and integration tests
├── data/                   # Local data and database location, if configured
├── requirements.txt        # Python dependencies
├── e2e_test.py             # End-to-end API tests
├── Dockerfile              # Container build configuration
├── railway.json            # Railway deployment configuration, if present
├── Procfile                # Process start configuration, if present
└── README.md               # Project documentation
```

Check the repository for the exact current filenames before relying on
optional files listed above.

## Run Locally in VS Code

### 1. Prerequisites

Install:

-   Python 3.12 (recommended for the supplied deployment configuration)
-   Visual Studio Code
-   Git
-   The Python extension for VS Code

### 2. Clone the repository

Open the VS Code terminal (`Terminal` → `New Terminal`) and run:

``` powershell
git clone https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent.git
cd ai-powered-maintenance-ticket-prioritization-agent
```

If the project is already on your computer, open its folder in VS Code
instead of cloning it again.

### 3. Create a virtual environment

On Windows PowerShell:

``` powershell
py -3.12 -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

``` bat
.venv\Scripts\activate.bat
```

If Python 3.12 is not installed, install it first. Use the Python
version supported by the project's dependency files.

### 4. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the application

Run Uvicorn from the repository root:

``` powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

Keep this terminal open while using the application.

### 6. Open the application

  Resource            Local URL
  ------------------- ----------------------------------
  Dashboard           http://127.0.0.1:8000/
  API documentation   http://127.0.0.1:8000/docs
  Health check        http://127.0.0.1:8000/api/health

The health endpoint should return a successful response with a healthy
status when the server and database are available.

### 7. Stop the server

In the terminal running Uvicorn, press:

``` text
Ctrl + C
```

### Alternative: use port 8001

If port `8000` is already occupied, start the app on port `8001`:

``` powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8001 --reload
```

Then open `http://127.0.0.1:8001/`.

## Configuration

The application uses environment-based configuration where supported by
the code. For deployment, the server should listen on the port provided
by the hosting platform.

Common settings to review in the repository:

-   `PORT`: the HTTP port assigned by the deployment platform.
-   `DB_PATH`: database file path, if supported by the current
    application code.

Do not commit secrets, access tokens, passwords, or production
credentials to GitHub. If your application requires environment
variables, configure them in your local environment or the hosting
provider's Variables settings.

## API Endpoints

The endpoints below are based on the project's reported API behavior.
Confirm the exact request schemas and response models in `/docs`,
because those are the authoritative definitions for the currently
deployed version.

  Method   Endpoint         Purpose
  -------- ---------------- -----------------------------------------
  `GET`    `/`              Serves the dashboard
  `GET`    `/api/health`    Reports application and database health
  `GET`    `/api/demo`      Returns demo or starter information
  `GET`    `/api/metrics`   Returns ticket and evaluation metrics
  `POST`   `/api/analyze`   Analyzes a maintenance ticket
  `POST`   `/api/tickets`   Creates a ticket

### Try the API

1.  Start the application.
2.  Open `http://127.0.0.1:8000/docs`.
3.  Expand an endpoint.
4.  Click **Try it out**.
5.  Enter a request body matching the schema displayed by Swagger UI.
6.  Click **Execute** and inspect the status code and response.

Use the request schema shown by the running API rather than copying an
example that may not match your current code.

## Evaluation

The current project report describes a small benchmark containing six
tickets:

  Metric                Reported result
  ------------------- -----------------
  Category accuracy          100% (6/6)
  Severity accuracy         83.3% (5/6)

**Interpretation:** These are reported results on a small benchmark, not
a guarantee of production accuracy. With only six examples, one
additional incorrect prediction changes the measured accuracy
substantially. Evaluate the system on a larger, representative,
independently labelled dataset before making claims about real-world
performance.

The evaluation panel in the dashboard can be used to view the available
benchmark results and the application's stated limitations.

## Testing

Run commands from the repository root with the virtual environment
activated.

### Unit and integration tests

``` powershell
python -m pytest tests/ -v
```

The project report previously stated that 13 tests passed. Run the
command above to confirm the result for your current checkout.

### End-to-end API tests

``` powershell
python e2e_test.py
```

The project report previously stated that 28 end-to-end checks passed.
Run the script to verify the current version. If it expects a running
server, start the application in a separate terminal first.

### Test checklist

-   [ ] Application starts without import errors.
-   [ ] `/api/health` returns a healthy response.
-   [ ] Dashboard loads in the browser.
-   [ ] `/docs` displays the OpenAPI documentation.
-   [ ] Ticket analysis returns a structured response.
-   [ ] Ticket creation behaves as expected.
-   [ ] Unit/integration tests pass.
-   [ ] End-to-end tests pass.

## Railway Deployment

The repository is configured for Railway deployment using a Docker-based
setup, according to the current project report.

1.  Push the latest working code to the `main` branch on GitHub.
2.  Open the Railway project connected to the repository.
3.  Select the web service.
4.  Open **Deployments** and check the latest deployment status.
5.  If a deployment does not start automatically, use the service's
    redeploy option.
6.  Review build and deploy logs. Confirm the service starts
    successfully.
7.  Open the generated public domain and test `/`, `/api/health`, and
    `/docs`.

**Port configuration:** A cloud service must bind to `0.0.0.0` and use
the port assigned through the `PORT` environment variable. The
repository's Dockerfile and application startup configuration should be
kept consistent. Prefer a straightforward, tested startup command over
argument-rewriting workarounds unless those workarounds are genuinely
required by the deployed configuration.

**Database persistence:** SQLite data may be lost when a container is
recreated if the database is stored on ephemeral container storage.
Configure a persistent volume and a suitable database path if ticket
data must survive redeployments, or use a managed database for a
production deployment.

The live links reported for this project are:

-   Dashboard: https://web-production-18808.up.railway.app/
-   Health check: https://web-production-18808.up.railway.app/api/health
-   API documentation: https://web-production-18808.up.railway.app/docs

Availability depends on the current Railway service and account status.

## Troubleshooting

### `ModuleNotFoundError` or dependency import errors

Activate the intended virtual environment and reinstall dependencies:

``` powershell
python -m pip install -r requirements.txt
```

Confirm that the selected Python interpreter in VS Code matches the
environment where the packages were installed.

### Port 8000 is already in use

Use port `8001`:

``` powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8001 --reload
```

### Railway reports a port error

-   Check the latest deploy logs.
-   Confirm the configured startup command uses the platform-provided
    `PORT`.
-   Confirm the application binds to `0.0.0.0` in production.
-   Check `Dockerfile`, `railway.json`, and `Procfile` for conflicting
    startup commands.
-   Redeploy only after correcting the configuration.

### Database is not connected

-   Check the configured database path and directory permissions.
-   Confirm the application can create or open the database file.
-   Review application logs for database exceptions.
-   For Railway, confirm the database path points to the intended
    persistent volume if persistence is required.

### The dashboard loads but API calls fail

-   Open the browser developer tools and inspect the Network tab.
-   Check the failed endpoint and HTTP status.
-   Open `/docs` to verify the available route and request schema.
-   Review the server logs for the underlying exception.

## Limitations and Responsible Use

-   Benchmark results are based on a small dataset and may not represent
    unseen maintenance scenarios.
-   Similarity-based classification depends on the quality and coverage
    of the reference examples.
-   Rule-based recommendations are only as reliable as the rules and
    data they use.
-   The application should not be the sole decision-maker for
    emergencies or safety-critical maintenance.
-   Review privacy, access control, validation, logging, and database
    persistence before using the system with real operational data.

## Future Improvements

-   Evaluate on a larger labelled dataset and report per-category
    precision, recall, and F1-score.
-   Add confidence estimates and a manual-review threshold for uncertain
    predictions.
-   Expand authentication, authorization, and audit logging as required.
-   Add richer ticket search, filters, status updates, and assignment
    workflows.
-   Add database migrations and persistent production storage.
-   Add CI checks for tests and deployment configuration.
-   Add dashboard screenshots and a short demonstration video.

## Author

**Shivasai Ankathi**

GitHub: [ankathishivasai9391](https://github.com/ankathishivasai9391)

Project repository: [AI-Powered Maintenance Ticket Prioritization
Agent](https://github.com/ankathishivasai9391/ai-powered-maintenance-ticket-prioritization-agent)

------------------------------------------------------------------------

*Documentation note: Keep this README aligned with the current
repository. Verify the project structure, endpoint schemas, test counts,
and deployment status whenever the code changes.*
