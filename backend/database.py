import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

from backend.config import DB_PATH, DATASET_PATH
from backend.data.dataset_loader import load_dataset
from backend.schemas import (
    TicketAnalysisResponse,
    TicketRecord,
    TicketListResponse,
    MetricsResponse,
    PriorityBreakdown,
    HistoricalMatch,
    TicketAnalysisRequest,
)

def get_db_connection() -> sqlite3.Connection:
    """Connect to SQLite database and configure row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create database tables and auto-seed benchmark data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            asset_id TEXT,
            category TEXT NOT NULL,
            category_label TEXT NOT NULL,
            severity TEXT NOT NULL,
            priority_score REAL NOT NULL,
            priority_label TEXT NOT NULL,
            priority_explanation TEXT,
            priority_breakdown_json TEXT NOT NULL,
            indicators_json TEXT NOT NULL,
            probable_root_cause TEXT NOT NULL,
            recommended_action TEXT NOT NULL,
            assigned_team TEXT NOT NULL,
            similar_tickets_json TEXT NOT NULL,
            safety_escalation INTEGER NOT NULL DEFAULT 0,
            safety_warning TEXT,
            human_review_required INTEGER NOT NULL DEFAULT 1,
            analysis_method TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_severity ON tickets(severity)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_asset_type ON tickets(asset_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at)")

    conn.commit()

    # Check if table is empty, if so, seed from benchmark CSV
    cursor.execute("SELECT COUNT(*) as cnt FROM tickets")
    row = cursor.fetchone()
    if row and row["cnt"] == 0:
        conn.close()
        seed_db_from_csv()
    else:
        conn.close()

def seed_db_from_csv():
    """Seed benchmark dataset from maintenance_tickets.csv into SQLite DB."""
    from backend.agent import agent

    # Load benchmark data as list of dicts
    records = load_dataset(DATASET_PATH)
    if not records:
        return

    for row in records:
        req = TicketAnalysisRequest(
            description=str(row.get("description", "")),
            asset_type=str(row.get("asset_type", "")),
            asset_id=f"ASSET-{row.get('ticket_id', '')}"
        )
        analysis = agent.analyze_ticket(req)
        # Override ticket_id with benchmark CSV ticket_id (T001, T002, etc.)
        save_ticket(analysis, custom_ticket_id=str(row.get("ticket_id", "")))
    
def row_to_ticket_record(row: sqlite3.Row) -> TicketRecord:
    """Helper to convert sqlite3.Row to Pydantic TicketRecord."""
    breakdown_dict = json.loads(row["priority_breakdown_json"])
    breakdown = PriorityBreakdown(**breakdown_dict)

    indicators = json.loads(row["indicators_json"])
    similar_raw = json.loads(row["similar_tickets_json"])
    similar_tickets = [HistoricalMatch(**m) for m in similar_raw]

    return TicketRecord(
        id=row["id"],
        ticket_id=row["ticket_id"],
        description=row["description"],
        asset_type=row["asset_type"],
        asset_id=row["asset_id"],
        category=row["category"],
        category_label=row["category_label"],
        severity=row["severity"],
        priority_score=float(row["priority_score"]),
        priority_label=row["priority_label"],
        priority_explanation=row["priority_explanation"],
        priority_breakdown=breakdown,
        indicators=indicators,
        probable_root_cause=row["probable_root_cause"],
        recommended_action=row["recommended_action"],
        assigned_team=row["assigned_team"],
        similar_tickets=similar_tickets,
        safety_escalation=bool(row["safety_escalation"]),
        safety_warning=row["safety_warning"],
        human_review_required=bool(row["human_review_required"]),
        analysis_method=row["analysis_method"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )

def save_ticket(analysis: TicketAnalysisResponse, custom_ticket_id: Optional[str] = None) -> TicketRecord:
    """Save an analyzed ticket record to SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).isoformat()
    ticket_id = custom_ticket_id or f"TCK-{int(datetime.now().timestamp() * 1000)}"

    breakdown_json = json.dumps(analysis.priority_breakdown.model_dump())
    indicators_json = json.dumps(analysis.indicators)
    similar_json = json.dumps([m.model_dump() for m in analysis.similar_tickets])

    cursor.execute("""
        INSERT INTO tickets (
            ticket_id, description, asset_type, asset_id, category, category_label,
            severity, priority_score, priority_label, priority_explanation,
            priority_breakdown_json, indicators_json, probable_root_cause,
            recommended_action, assigned_team, similar_tickets_json, safety_escalation,
            safety_warning, human_review_required, analysis_method, status,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, 'open',
            ?, ?
        )
    """, (
        ticket_id, analysis.description, analysis.asset_type, analysis.asset_id, analysis.category, analysis.category_label,
        analysis.severity, analysis.priority_score, analysis.priority_label, analysis.priority_explanation,
        breakdown_json, indicators_json, analysis.probable_root_cause,
        analysis.recommended_action, analysis.assigned_team, similar_json, 1 if analysis.safety_escalation else 0,
        analysis.safety_warning, 1 if analysis.human_review_required else 0, analysis.analysis_method,
        analysis.created_at or now_str, now_str
    ))

    conn.commit()
    row_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (row_id,))
    saved_row = cursor.fetchone()
    conn.close()

    return row_to_ticket_record(saved_row)

def get_ticket_by_id(ticket_id: str) -> Optional[TicketRecord]:
    """Retrieve ticket by ticket_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ? OR id = ?", (ticket_id, ticket_id if ticket_id.isdigit() else -1))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_ticket_record(row)
    return None

def list_tickets(
    asset_type: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 50
) -> TicketListResponse:
    """List tickets with filtering, searching, and pagination."""
    conn = get_db_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if asset_type and asset_type.strip() and asset_type.lower() != "all":
        conditions.append("LOWER(asset_type) = LOWER(?)")
        params.append(asset_type.strip())

    if severity and severity.strip() and severity.lower() != "all":
        conditions.append("LOWER(severity) = LOWER(?)")
        params.append(severity.strip())

    if status and status.strip() and status.lower() != "all":
        conditions.append("LOWER(status) = LOWER(?)")
        params.append(status.strip())

    if search and search.strip():
        term = f"%{search.strip().lower()}%"
        conditions.append("(LOWER(description) LIKE ? OR LOWER(ticket_id) LIKE ? OR LOWER(category_label) LIKE ? OR LOWER(asset_id) LIKE ?)")
        params.extend([term, term, term, term])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    cursor.execute(f"SELECT COUNT(*) as total FROM tickets{where_clause}", params)
    total = cursor.fetchone()["total"]

    offset = (page - 1) * limit
    cursor.execute(f"SELECT * FROM tickets{where_clause} ORDER BY priority_score DESC, id DESC LIMIT ? OFFSET ?", params + [limit, offset])
    rows = cursor.fetchall()
    conn.close()

    tickets = [row_to_ticket_record(r) for r in rows]
    return TicketListResponse(
        total=total,
        page=page,
        limit=limit,
        tickets=tickets
    )

def update_ticket_status(ticket_id: str, new_status: str) -> Optional[TicketRecord]:
    """Update ticket workflow status."""
    conn = get_db_connection()
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("UPDATE tickets SET status = ?, updated_at = ? WHERE ticket_id = ? OR id = ?", (new_status, now_str, ticket_id, ticket_id if ticket_id.isdigit() else -1))
    conn.commit()

    conn.close()
    return get_ticket_by_id(ticket_id)

def update_ticket_team(ticket_id: str, new_team: str) -> Optional[TicketRecord]:
    """Update ticket assigned team."""
    conn = get_db_connection()
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).isoformat()
    cursor.execute("UPDATE tickets SET assigned_team = ?, updated_at = ? WHERE ticket_id = ? OR id = ?", (new_team, now_str, ticket_id, ticket_id if ticket_id.isdigit() else -1))
    conn.commit()

    conn.close()
    return get_ticket_by_id(ticket_id)

def delete_ticket(ticket_id: str) -> bool:
    """Delete a ticket by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE ticket_id = ? OR id = ?", (ticket_id, ticket_id if ticket_id.isdigit() else -1))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def get_metrics() -> MetricsResponse:
    """Aggregate tickets metrics and analytics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM tickets")
    total_tickets = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE status != 'closed' AND status != 'resolved'")
    open_tickets = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE severity = 'critical'")
    critical_tickets = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE priority_score >= 60.0")
    high_priority_tickets = cursor.fetchone()["cnt"]

    cursor.execute("SELECT AVG(priority_score) as avg_score FROM tickets")
    avg_row = cursor.fetchone()
    avg_priority_score = round(avg_row["avg_score"] or 0.0, 1)

    # Severity distribution
    cursor.execute("SELECT severity, COUNT(*) as cnt FROM tickets GROUP BY severity")
    sev_rows = cursor.fetchall()
    severity_distribution = {r["severity"]: r["cnt"] for r in sev_rows}

    # Category distribution
    cursor.execute("SELECT category, COUNT(*) as cnt FROM tickets GROUP BY category")
    cat_rows = cursor.fetchall()
    category_distribution = {r["category"]: r["cnt"] for r in cat_rows}

    # Team workload
    cursor.execute("SELECT assigned_team, COUNT(*) as cnt FROM tickets GROUP BY assigned_team")
    team_rows = cursor.fetchall()
    team_workload = {r["assigned_team"]: r["cnt"] for r in team_rows}

    # Recent tickets
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 5")
    recent_rows = cursor.fetchall()
    conn.close()

    recent_tickets = [row_to_ticket_record(r) for r in recent_rows]

    return MetricsResponse(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        critical_tickets=critical_tickets,
        high_priority_tickets=high_priority_tickets,
        avg_priority_score=avg_priority_score,
        severity_distribution=severity_distribution,
        category_distribution=category_distribution,
        team_workload=team_workload,
        recent_tickets=recent_tickets,
    )
