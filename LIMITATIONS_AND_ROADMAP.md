# Limitations & Roadmap

This document provides an honest assessment of the current system's constraints and a prioritised roadmap for future development.

---

## Current Limitations

### 1. Small Benchmark Dataset
- **Constraint:** Evaluation is performed against only 6 hand-labeled samples.
- **Impact:** Accuracy metrics (100% category, 83.3% severity) cannot be considered statistically significant.
- **Honest assessment:** Results should be interpreted as a proof-of-concept demonstration, not production-grade validation.

### 2. No Real-Time Sensor Integration
- **Constraint:** The agent processes free-text descriptions only. It does not ingest live SCADA telemetry, IoT sensor streams, or time-series data.
- **Impact:** Early-warning detection (e.g., gradual vibration increase over time) is not possible in the current architecture.

### 3. Rule-Based Severity Scoring
- **Constraint:** Severity estimation relies on keyword heuristics and domain rules. The rules were hand-crafted for the renewable energy domain.
- **Impact:** Edge cases — particularly ambiguous multi-symptom descriptions — may be misclassified. (e.g., T003 in the benchmark: over-escalated to `high` instead of `medium`.)
- **Honest assessment:** A fine-tuned classification model or LLM would outperform the rule engine on diverse real-world tickets.

### 4. SQLite — Not Horizontally Scalable
- **Constraint:** The database layer uses SQLite, a single-file embedded database.
- **Impact:** Concurrent writes from multiple workers will cause locking conflicts. Cannot run behind a load balancer with multiple replicas.
- **Production fix:** Migrate to PostgreSQL or another server-based RDBMS.

### 5. No Authentication or Access Control
- **Constraint:** The API has no authentication mechanism. All endpoints are publicly accessible.
- **Impact:** Not suitable for production deployment without adding an auth layer.
- **Production fix:** Implement OAuth2 / JWT bearer token authentication via FastAPI's security utilities.

### 6. No LLM Integration
- **Constraint:** The agent uses TF-IDF + rules, not a large language model.
- **Impact:** Root-cause narratives are template-based. The agent cannot reason about novel failure modes it has not seen before.

### 7. Single-Language Support
- **Constraint:** Only English-language descriptions are supported. Non-English tickets will produce low similarity scores and fall back to heuristics.

---

## Roadmap

### Near-Term (v1.1 — Next Sprint)

| Priority | Feature | Description |
|:---|:---|:---|
| 🔴 High | Expand benchmark dataset | Increase to ≥50 labeled samples with cross-validation split |
| 🔴 High | PostgreSQL support | Replace SQLite with PostgreSQL for production scalability |
| 🟠 Medium | API authentication | Add JWT bearer token auth with user/role management |
| 🟠 Medium | Improved severity model | Train a lightweight multi-class classifier on expanded dataset |

### Mid-Term (v2.0 — Future Release)

| Priority | Feature | Description |
|:---|:---|:---|
| 🟠 Medium | LLM integration | Integrate Gemini or GPT-4o for richer root-cause narratives and reasoning chains |
| 🟠 Medium | Real-time SCADA feed | WebSocket or MQTT adapter to ingest live sensor readings |
| 🟡 Low | Email/Slack notifications | Alert assigned teams when a `critical` ticket is created |
| 🟡 Low | Multi-language support | Extend preprocessing to support Spanish, German (common in EU energy sector) |
| 🟡 Low | Mobile-responsive UI | Enhance dashboard layout for tablet and mobile viewports |

### Long-Term (v3.0 — Enterprise)

| Priority | Feature | Description |
|:---|:---|:---|
| 🟡 Low | Agentic tool-use | Give the agent tools to query maintenance logs, look up asset history, and draft work orders |
| 🟡 Low | Predictive maintenance | Forecast failure probability from historical sensor trends |
| 🟡 Low | Multi-tenant SaaS | Isolate data per organisation with tenant-scoped API keys |

---

## Responsible Use Statement

This system is a **decision-support tool**, not an autonomous decision-maker. It is designed to help maintenance engineers prioritize their work queue faster — not to replace human judgement.

Before acting on any recommendation from this agent for safety-critical equipment:
1. A qualified maintenance engineer must review the recommendation.
2. Standard safety protocols and site-specific procedures take precedence.
3. Critical-severity tickets should always trigger a physical inspection before any remote action.

The authors accept no liability for decisions made solely on the basis of this tool's output without human review.
