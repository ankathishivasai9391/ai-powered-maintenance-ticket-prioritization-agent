from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

class Query(BaseModel):
    """Starter legacy query model for backwards compatibility with /api/run."""
    text: str = ""

class TicketAnalysisRequest(BaseModel):
    """Input payload for ticket analysis."""
    description: str = Field(..., description="Observed fault report text", min_length=3, max_length=2000)
    asset_type: Optional[str] = Field(None, description="Type of asset (e.g. solar, wind, hydro, grid)")
    asset_id: Optional[str] = Field(None, description="Asset identifier e.g. WTG-12, INV-04")

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Ticket description cannot be blank or whitespace only.")
        return cleaned

class TicketCreateRequest(TicketAnalysisRequest):
    """Payload to analyze and persist a new ticket."""
    pass

class TicketStatusUpdate(BaseModel):
    """Payload to update workflow status."""
    status: str = Field(..., description="New workflow status: open, in_progress, resolved, escalated, closed")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = {"open", "in_progress", "resolved", "escalated", "closed"}
        cleaned = v.strip().lower()
        if cleaned not in valid_statuses:
            raise ValueError(f"Invalid status '{v}'. Allowed: {', '.join(sorted(valid_statuses))}")
        return cleaned

class TicketAssignmentUpdate(BaseModel):
    """Payload to update assigned team."""
    team: str = Field(..., description="Assigned team name")

    @field_validator('team')
    @classmethod
    def validate_team(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Team name cannot be empty.")
        return cleaned

class PriorityBreakdown(BaseModel):
    base_severity_score: float
    modifiers: List[str]
    final_score: float

class HistoricalMatch(BaseModel):
    ticket_id: str
    asset_type: str
    description: str
    target_severity: str
    target_category: str
    similarity_score: float

class TicketAnalysisResponse(BaseModel):
    ticket_id: Optional[str] = None
    description: str
    asset_type: str
    asset_id: Optional[str] = None
    category: str
    category_label: str
    severity: str
    priority_score: float
    priority_label: str
    priority_explanation: str
    priority_breakdown: PriorityBreakdown
    indicators: List[str]
    probable_root_cause: str
    recommended_action: str
    assigned_team: str
    similar_tickets: List[HistoricalMatch]
    safety_escalation: bool
    safety_warning: Optional[str] = None
    human_review_required: bool = True
    analysis_method: str
    created_at: str

class TicketRecord(TicketAnalysisResponse):
    id: int
    ticket_id: str
    status: str = "open"
    updated_at: str

class TicketListResponse(BaseModel):
    total: int
    page: int
    limit: int
    tickets: List[TicketRecord]

class MetricsResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    critical_tickets: int
    high_priority_tickets: int
    avg_priority_score: float
    severity_distribution: Dict[str, int]
    category_distribution: Dict[str, int]
    team_workload: Dict[str, int]
    recent_tickets: List[TicketRecord]

class EvaluationResponse(BaseModel):
    total_labeled_examples: int
    category_accuracy: float
    category_correct: int
    severity_accuracy: float
    severity_correct: int
    method: str
    limitations: List[str]
    confusion_matrix: Optional[Dict[str, Any]] = None
