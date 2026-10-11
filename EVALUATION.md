# Evaluation Report — AI-Powered Maintenance Ticket Prioritization Agent

## Summary

| Metric | Result |
|:---|:---|
| **Category Accuracy** | **100.0%** (6 / 6 correct) |
| **Severity Accuracy** | **83.3%** (5 / 6 correct) |
| **Evaluation Dataset** | `data/maintenance_tickets.csv` |
| **Total Labeled Samples** | 6 |
| **Evaluation Method** | TF-IDF Cosine Similarity + Hybrid Rule-Based Expert System |

---

## Methodology

### How Evaluation Works

1. **Load benchmark CSV** — The agent reads `data/maintenance_tickets.csv`, which contains 6 hand-labeled maintenance tickets with known `category` and `severity` ground-truth values.
2. **Re-run agent analysis** — Each ticket description is passed through the full AI pipeline:  TF-IDF vectorization → cosine similarity → hybrid rule engine → structured output.
3. **Compare predictions** — Predicted category and severity are compared against ground-truth labels.
4. **Report metrics** — Category accuracy, severity accuracy, and per-ticket confusion data are returned via `/api/evaluation` and rendered live in the dashboard.

### Pipeline Components

```
  Input Description
        │
        ▼
  TF-IDF Vectorizer (scikit-learn or pure-Python fallback)
  + Cosine Similarity against 10 category reference documents
        │
        ▼
  Top Category Match  →  Hybrid Rule Engine
                         · Energy-domain keyword signals
                         · Asset-type severity modifiers
                         · Fault keyword severity boosters
                         · Duration and criticality rules
        │
        ▼
  Predicted: category, severity, priority_score, team, action
```

---

## Per-Ticket Confusion Matrix

| Ticket ID | True Category | Predicted | ✓ | True Severity | Predicted | ✓ |
|:---|:---|:---|:---:|:---|:---|:---:|
| T001 | `inverter_thermal` | `inverter_thermal` | ✅ | `high` | `high` | ✅ |
| T002 | `gearbox_vibration` | `gearbox_vibration` | ✅ | `critical` | `critical` | ✅ |
| T003 | `inspection_compliance` | `inspection_compliance` | ✅ | `medium` | `high` | ❌ |
| T004 | `data_gap` | `data_gap` | ✅ | `medium` | `medium` | ✅ |
| T005 | `pitch_system` | `pitch_system` | ✅ | `high` | `high` | ✅ |
| T006 | `grid_curtailment` | `grid_curtailment` | ✅ | `medium` | `medium` | ✅ |

**Category: 6/6 correct (100.0%)**  
**Severity: 5/6 correct (83.3%)** — T003 predicted `high` vs. ground-truth `medium`

---

## Analysis of Misclassification

### T003 — Inspection Compliance (Severity Mismatch)

**Ticket description:** *"Routine quarterly inspection overdue for wind turbine WT-009 in Sector B. Last inspection recorded 6 months ago — compliance risk."*

| Aspect | Value |
|:---|:---|
| **True Severity** | `medium` |
| **Predicted Severity** | `high` |
| **Root Cause** | The phrase *"compliance risk"* triggers the `high`-severity compliance rule in the expert system, which was designed conservatively to escalate regulatory issues. |
| **Impact** | Low — over-escalation is safer than under-escalation for compliance tickets. |
| **Fix** | Introduce a time-since-last-inspection duration signal to distinguish regulatory overdue from acute safety risk. |

---

## Benchmark Dataset

Located at `data/maintenance_tickets.csv`. Sample structure:

```csv
ticket_id,description,true_category,true_severity
T001,"Solar inverter at Site A showing intermittent overheating...",inverter_thermal,high
T002,"Gearbox vibration detected on wind turbine WT-007...",gearbox_vibration,critical
T003,"Routine quarterly inspection overdue for WT-009...",inspection_compliance,medium
T004,"SCADA data gap for turbines WT-003 and WT-004...",data_gap,medium
T005,"Pitch system malfunction causing blade angle control failure...",pitch_system,high
T006,"Grid curtailment notification received from operator...",grid_curtailment,medium
```

---

## Live Evaluation API

```bash
GET /api/evaluation
```

**Response:**

```json
{
  "total_labeled_examples": 6,
  "category_accuracy": 1.0,
  "category_correct": 6,
  "severity_accuracy": 0.8333,
  "severity_correct": 5,
  "method": "TF-IDF Cosine Similarity Vectorizer + Hybrid Rule-based Expert Agent",
  "limitations": [
    "Small benchmark evaluation sample size (6 items)...",
    "Edge case descriptions with ambiguous multi-asset fault reports...",
    "No real-time SCADA telemetry sensor stream integration..."
  ]
}
```

---

## Limitations of the Evaluation

1. **Small sample size** — 6 labeled examples is insufficient to claim statistical significance. A production system requires ≥100 diverse samples per category.
2. **Self-referential data** — The benchmark CSV was used to construct some of the agent's reference corpus, which may inflate accuracy metrics.
3. **No cross-validation** — A single train/test split was not applied; evaluation is purely against labeled ground-truth.
4. **Domain narrowness** — All samples are from the renewable energy domain. Performance may degrade on general facility maintenance tickets.

---

*Evaluation is computed live by the agent on every `/api/evaluation` call. Run `python e2e_test.py` to validate end-to-end.*
