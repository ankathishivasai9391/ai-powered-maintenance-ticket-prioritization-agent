from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query as FastAPIQuery, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.agent import agent
from backend.config import BASE_DIR
from backend.database import (
    init_db,
    save_ticket,
    get_ticket_by_id,
    list_tickets,
    update_ticket_status,
    update_ticket_team,
    delete_ticket,
    get_metrics,
    seed_db_from_csv,
)
from backend.schemas import (
    Query as LegacyQuery,
    TicketAnalysisRequest,
    TicketCreateRequest,
    TicketAnalysisResponse,
    TicketRecord,
    TicketListResponse,
    TicketStatusUpdate,
    TicketAssignmentUpdate,
    MetricsResponse,
    EvaluationResponse,
)

FRONTEND_DIR = BASE_DIR / "frontend"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema and seed benchmark data if empty
    init_db()
    yield

app = FastAPI(
    title="AI Agent for Maintenance Ticket Prioritization",
    description="Enterprise Renewable Maintenance Ticket Prioritization Agent API",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for cross-origin local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend static files if present
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/", include_in_schema=False)
def read_root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "AI Agent for Maintenance Ticket Prioritization API running."}

@app.get("/api/demo")
def demo():
    """Preserved starter demo endpoint."""
    return {
        "case_study": "AI Agent for Maintenance Ticket Prioritization",
        "status": "starter app running",
        "expected_outcome": "A ticket triage system that assigns severity, category, probable root cause, and next action using NLP and rule/tool-based agent logic."
    }

@app.get("/api/health")
def health_check():
    """Real health check endpoint verifying database connectivity."""
    try:
        metrics = get_metrics()
        return {
            "status": "healthy",
            "service": "AI Maintenance Ticket Prioritization Agent",
            "database": "connected",
            "total_tickets": metrics.total_tickets
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unreachable: {str(e)}"
        )

@app.post("/api/run")
def run_case(query: LegacyQuery):
    """
    Preserved starter endpoint for compatibility.
    Analyzes query text and returns prioritized triage analysis.
    """
    if not query.text or not query.text.strip():
        req = TicketAnalysisRequest(description="Routine inspection pending")
    else:
        req = TicketAnalysisRequest(description=query.text)

    analysis = agent.analyze_ticket(req)

    return {
        "input": query.text,
        "result": f"Priority: {analysis.priority_label} (Score: {analysis.priority_score}) | Category: {analysis.category_label}",
        "analysis": analysis.model_dump(),
        "evaluation_hint": "Return predictions, retrieval evidence, reasoning steps, metrics, and limitations."
    }

@app.post("/api/analyze", response_model=TicketAnalysisResponse)
def analyze_ticket_endpoint(request: TicketAnalysisRequest):
    """On-the-fly ticket analysis without DB persistence."""
    return agent.analyze_ticket(request)

@app.post("/api/tickets", response_model=TicketRecord, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(request: TicketCreateRequest):
    """Analyze and persist a new maintenance ticket in SQLite."""
    analysis = agent.analyze_ticket(request)
    ticket_record = save_ticket(analysis)
    return ticket_record

@app.get("/api/tickets", response_model=TicketListResponse)
def get_tickets_endpoint(
    asset_type: Optional[str] = FastAPIQuery(None, description="Filter by asset type"),
    severity: Optional[str] = FastAPIQuery(None, description="Filter by severity"),
    status_filter: Optional[str] = FastAPIQuery(None, alias="status", description="Filter by status"),
    search: Optional[str] = FastAPIQuery(None, description="Search term in description or ID"),
    page: int = FastAPIQuery(1, ge=1, description="Page number"),
    limit: int = FastAPIQuery(50, ge=1, le=100, description="Page limit"),
):
    """List tickets with filtering, search, and pagination."""
    return list_tickets(
        asset_type=asset_type,
        severity=severity,
        status=status_filter,
        search=search,
        page=page,
        limit=limit,
    )

@app.get("/api/tickets/{ticket_id}", response_model=TicketRecord)
def get_single_ticket_endpoint(ticket_id: str):
    """Retrieve details for a specific ticket by ticket_id or database ID."""
    record = get_ticket_by_id(ticket_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket '{ticket_id}' not found."
        )
    return record

@app.patch("/api/tickets/{ticket_id}/status", response_model=TicketRecord)
def update_ticket_status_endpoint(ticket_id: str, update: TicketStatusUpdate):
    """Update workflow status of a ticket."""
    record = update_ticket_status(ticket_id, update.status)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket '{ticket_id}' not found."
        )
    return record

@app.patch("/api/tickets/{ticket_id}/assign", response_model=TicketRecord)
def update_ticket_assignment_endpoint(ticket_id: str, update: TicketAssignmentUpdate):
    """Reassign ticket to a new maintenance team."""
    record = update_ticket_team(ticket_id, update.team)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket '{ticket_id}' not found."
        )
    return record

@app.delete("/api/tickets/{ticket_id}")
def delete_ticket_endpoint(ticket_id: str):
    """Delete a ticket by ID."""
    success = delete_ticket(ticket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket '{ticket_id}' not found."
        )
    return {"message": "Ticket deleted successfully.", "ticket_id": ticket_id}

@app.get("/api/metrics", response_model=MetricsResponse)
def get_metrics_endpoint():
    """Retrieve system dashboard metrics and workload analytics."""
    return get_metrics()

@app.get("/api/evaluation", response_model=EvaluationResponse)
def get_evaluation_endpoint():
    """Retrieve model evaluation metrics evaluated against benchmark data."""
    eval_dict = agent.evaluate_benchmark()
    return EvaluationResponse(**eval_dict)

@app.post("/api/seed")
def seed_tickets_endpoint():
    """Re-seed SQLite database with benchmark tickets."""
    seed_db_from_csv()
    agent.reload_dataset()
    return {"message": "Database successfully seeded with benchmark dataset."}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)

