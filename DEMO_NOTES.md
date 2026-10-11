# Demo Guide — AI-Powered Maintenance Ticket Prioritization Agent

> **For reviewers and assessors.** This guide takes approximately 5–7 minutes to complete and covers all key features of the application.

---

## Prerequisites

Either:
- **Live deployment**: https://ai-powered-maintenance-ticket-prioritization-agent-production.up.railway.app/
- **Local setup**: Follow `README.md` Quick Start → server running at `http://127.0.0.1:8000/`

---

## Step-by-Step Demo

### Step 1 — Open the Dashboard

Navigate to the root URL. You should see:
- A header with the application title and action buttons
- KPI metric cards (Total Tickets, Critical, High severity counts)
- The ticket queue table (empty on first run)
- The Evaluation panel at the bottom

> If the ticket table is empty, click **"Reset / Seed Benchmark Dataset"** in the top-right header area.

---

### Step 2 — Submit a New Maintenance Ticket (AI Analysis)

Locate the **"Submit New Ticket"** form panel on the dashboard.

**Paste this description:**

```
Wind turbine WT-012 gearbox is producing an unusual grinding sound and
vibration level has exceeded 8.5 mm/s RMS. Bearing temperature reached
92°C. Immediate inspection required before catastrophic failure.
```

Select asset type: **Wind Turbine** and click **Analyze & Submit**.

**Expected output:**
| Field | Expected Value |
|:---|:---|
| Category | `gearbox_vibration` |
| Severity | `critical` |
| Priority Score | 90–100 |
| Recommended Team | Mechanical / Gearbox Team |
| Next Action | Immediate shutdown + inspection |

---

### Step 3 — Submit a Low-Priority Ticket

**Paste this description:**

```
Quarterly SCADA data export for solar farm SF-04 is scheduled for
next week. Ensure data logging is active and export configuration
is confirmed with the data team.
```

Select asset type: **Solar** and click **Analyze & Submit**.

**Expected output:**
| Field | Expected Value |
|:---|:---|
| Category | `data_gap` or `inspection_compliance` |
| Severity | `low` or `medium` |
| Priority Score | 10–35 |

> Notice how the priority score contrast demonstrates the agent's ability to differentiate urgency levels.

---

### Step 4 — Explore the Ticket Queue

In the ticket table:
- **Filter by severity** using the dropdown — try "Critical"
- **Search** for a keyword (e.g., "gearbox")
- **Click any row** to open the Detail Modal — observe the priority score breakdown

---

### Step 5 — Update a Ticket Status

In the ticket table, locate the status dropdown for any ticket.  
Change it from `open` → `in_progress` → `resolved`.

The change is persisted immediately to the SQLite database via `PATCH /api/tickets/{id}/status`.

---

### Step 6 — View the Evaluation Panel

Scroll to the bottom of the dashboard.

The **Evaluation Panel** shows:
- **Left box (mint green):** Benchmark Validation Accuracy metrics
  - Category Accuracy: 100.0%
  - Severity Accuracy: 83.3%
- **Right box (amber):** Production Limitations & Recommendations

Click **"Refresh Evaluation"** to re-run the live benchmark evaluation.

---

### Step 7 — Explore the API (Swagger UI)

Navigate to `/docs` on your deployment URL.

Try these live endpoints:
1. `GET /api/health` — Verify service health
2. `POST /api/analyze` — Submit raw JSON for instant analysis (no DB write)
3. `GET /api/evaluation` — View full benchmark JSON response
4. `GET /api/metrics` — Retrieve dashboard KPI data

**Sample request body for `POST /api/analyze`:**

```json
{
  "description": "Solar inverter overheating at site B, output dropped by 40%",
  "asset_type": "solar",
  "asset_id": "INV-021"
}
```

---

## What to Highlight to the Reviewer

| Capability | Where to Show |
|:---|:---|
| AI classification | Submit form → observe structured output |
| Priority scoring | Detail modal → Priority Breakdown section |
| Live evaluation | Bottom panel → Refresh Evaluation button |
| Full REST API | `/docs` Swagger UI |
| Ticket persistence | Submit, then filter/search in the queue |
| Status workflow | Status dropdown in ticket row |
| Docker deployment | `Dockerfile` in repository root |

---

## Troubleshooting

| Issue | Fix |
|:---|:---|
| Empty ticket table | Click "Reset / Seed Benchmark Dataset" |
| 502 error on Railway | Wait 30s for cold-start, then refresh |
| Port in use locally | Use `--port 8001` in the uvicorn command |
| Import errors | Ensure `.venv` is activated and `pip install -r requirements.txt` ran successfully |
