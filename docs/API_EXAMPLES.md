# API Examples — AI-Powered Maintenance Ticket Prioritization Agent

> **Base URL (production):** `https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app`  
> **Base URL (local):** `http://127.0.0.1:8000`

Interactive docs: append `/docs` to either URL.

---

## Health Check

### cURL
```bash
curl https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/health
```

### Response
```json
{
  "status": "healthy",
  "service": "AI Maintenance Ticket Prioritization Agent",
  "database": "connected",
  "total_tickets": 6
}
```

---

## Analyze a Ticket (No Persistence)

### cURL
```bash
curl -X POST \
  https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Wind turbine gearbox producing grinding noise, vibration at 9.2 mm/s RMS, bearing temp 95C",
    "asset_type": "wind_turbine",
    "asset_id": "WT-042"
  }'
```

### Python (requests)
```python
import requests

BASE_URL = "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app"

response = requests.post(f"{BASE_URL}/api/analyze", json={
    "description": "Wind turbine gearbox producing grinding noise, vibration at 9.2 mm/s RMS, bearing temp 95C",
    "asset_type": "wind_turbine",
    "asset_id": "WT-042"
})
print(response.json())
```

### Response
```json
{
  "ticket_id": null,
  "description": "Wind turbine gearbox producing grinding noise...",
  "asset_type": "wind_turbine",
  "asset_id": "WT-042",
  "category": "gearbox_vibration",
  "category_label": "Gearbox Vibration / Bearing Fault",
  "severity": "critical",
  "priority_score": 98,
  "priority_label": "CRITICAL",
  "priority_breakdown": {
    "base_severity_score": 90,
    "modifiers": [
      "Asset type modifier (wind_turbine): +5",
      "Vibration keyword detected: +3"
    ]
  },
  "probable_root_cause": "Gearbox bearing wear or lubrication failure causing mechanical resonance",
  "recommended_action": "Immediate shutdown and full gearbox inspection by mechanical team",
  "assigned_team": "Mechanical / Gearbox Team",
  "similarity_score": 0.89,
  "retrieval_evidence": ["gearbox vibration bearing fault wind turbine..."]
}
```

---

## Create & Persist a New Ticket

### cURL
```bash
curl -X POST \
  https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Solar inverter at Site C showing overheating warning. Output dropped 35%. Ambient temp 42C.",
    "asset_type": "solar",
    "asset_id": "INV-017"
  }'
```

### Response (HTTP 201)
```json
{
  "id": 7,
  "ticket_id": "TKT-20261011-0007",
  "description": "Solar inverter at Site C showing overheating warning...",
  "asset_type": "solar",
  "asset_id": "INV-017",
  "category": "inverter_thermal",
  "category_label": "Inverter Thermal / Overheating",
  "severity": "high",
  "priority_score": 82,
  "priority_label": "HIGH",
  "assigned_team": "Electrical / Inverter Team",
  "status": "open",
  "created_at": "2026-10-11T08:30:00Z",
  "updated_at": "2026-10-11T08:30:00Z"
}
```

---

## List Tickets with Filters

### All tickets
```bash
curl "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets"
```

### Filter by severity
```bash
curl "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets?severity=critical"
```

### Filter by asset type + status
```bash
curl "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets?asset_type=wind_turbine&status=open"
```

### Search + paginate
```bash
curl "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets?search=gearbox&page=1&limit=10"
```

---

## Get a Single Ticket

```bash
curl https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets/TKT-20261011-0001
```

---

## Update Ticket Status

```bash
curl -X PATCH \
  https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets/TKT-20261011-0001/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

**Valid status values:** `open`, `in_progress`, `resolved`, `closed`

---

## Reassign Ticket to a Team

```bash
curl -X PATCH \
  https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/tickets/TKT-20261011-0001/assign \
  -H "Content-Type: application/json" \
  -d '{"team": "Electrical / Inverter Team"}'
```

---

## Get Dashboard Metrics

```bash
curl https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/metrics
```

### Response
```json
{
  "total_tickets": 6,
  "open_tickets": 4,
  "critical_tickets": 1,
  "high_tickets": 2,
  "medium_tickets": 2,
  "low_tickets": 1,
  "by_category": {
    "gearbox_vibration": 1,
    "inverter_thermal": 1,
    "pitch_system": 1,
    "data_gap": 1,
    "inspection_compliance": 1,
    "grid_curtailment": 1
  }
}
```

---

## Get Evaluation Results

```bash
curl https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/evaluation
```

---

## Seed Benchmark Data

```bash
curl -X POST \
  https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/api/seed
```

---

## Python Full Example — Analyze + Create + List

```python
import requests

BASE = "https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app"

# 1. Analyze a ticket without saving
analysis = requests.post(f"{BASE}/api/analyze", json={
    "description": "Pitch system malfunction on WT-005, blade angle unresponsive in high wind",
    "asset_type": "wind_turbine",
    "asset_id": "WT-005"
}).json()
print(f"Category: {analysis['category_label']}, Severity: {analysis['severity']}, Score: {analysis['priority_score']}")

# 2. Save the ticket
ticket = requests.post(f"{BASE}/api/tickets", json={
    "description": "Pitch system malfunction on WT-005, blade angle unresponsive in high wind",
    "asset_type": "wind_turbine",
    "asset_id": "WT-005"
}).json()
print(f"Created: {ticket['ticket_id']} — {ticket['assigned_team']}")

# 3. Update status
requests.patch(f"{BASE}/api/tickets/{ticket['ticket_id']}/status", json={"status": "in_progress"})

# 4. List all critical open tickets
queue = requests.get(f"{BASE}/api/tickets", params={"severity": "critical", "status": "open"}).json()
print(f"Critical open tickets: {queue['total']}")
```
