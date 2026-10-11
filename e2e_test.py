"""End-to-end API test script for the Maintenance Ticket Prioritization Agent."""
import urllib.request
import json
import sys

BASE = "http://127.0.0.1:8000"

def api_get(path):
    r = urllib.request.urlopen(f"{BASE}{path}")
    return json.loads(r.read())

def api_post(path, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=body, headers={"Content-Type": "application/json"})
    r = urllib.request.urlopen(req)
    return json.loads(r.read())

def api_patch(path, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=body, headers={"Content-Type": "application/json"}, method="PATCH")
    r = urllib.request.urlopen(req)
    return json.loads(r.read())

def api_delete(path):
    req = urllib.request.Request(f"{BASE}{path}", method="DELETE")
    r = urllib.request.urlopen(req)
    return json.loads(r.read())

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name} -- {detail}")

print("=" * 60)
print("END-TO-END API TEST")
print("=" * 60)

# 1. Demo endpoint
print("\n[1] GET /api/demo")
d = api_get("/api/demo")
check("Status 200 + correct case_study", d.get("case_study") == "AI Agent for Maintenance Ticket Prioritization")

# 2. Run endpoint
print("\n[2] POST /api/run")
d = api_post("/api/run", {"text": "Inverter 4 tripping repeatedly after noon"})
check("Has result field", "result" in d)
check("Has analysis field", "analysis" in d)
check("Category is inverter_thermal", d["analysis"]["category"] == "inverter_thermal", d["analysis"].get("category"))

# 3. Analyze endpoint
print("\n[3] POST /api/analyze")
d = api_post("/api/analyze", {
    "description": "Gearbox vibration has increased for turbine WTG-12 with abnormal noise",
    "asset_type": "wind",
    "asset_id": "WTG-12"
})
check("Severity is critical", d["severity"] == "critical", d.get("severity"))
check("Priority label is CRITICAL", d["priority_label"] == "CRITICAL", d.get("priority_label"))
check("Assigned to Wind Mechanical Maintenance", d["assigned_team"] == "Wind Mechanical Maintenance", d.get("assigned_team"))

# 4. List tickets (seeded)
print("\n[4] GET /api/tickets")
d = api_get("/api/tickets")
total = d["total"]
check(f"Seeded tickets exist (total={total})", total >= 6)

# 5. Create a new ticket
print("\n[5] POST /api/tickets (create)")
d = api_post("/api/tickets", {
    "description": "Inspection checklist pending for spillway gate maintenance",
    "asset_type": "hydro",
    "asset_id": "HYD-SP-01"
})
new_id = d["ticket_id"]
check(f"Ticket created with id={new_id}", d["status"] == "open")

# 6. Get single ticket
print("\n[6] GET /api/tickets/{id}")
d = api_get(f"/api/tickets/{new_id}")
check("Retrieved ticket matches", d["asset_id"] == "HYD-SP-01")

# 7. Patch status
print("\n[7] PATCH /api/tickets/{id}/status")
d = api_patch(f"/api/tickets/{new_id}/status", {"status": "in_progress"})
check("Status updated to in_progress", d["status"] == "in_progress", d.get("status"))

# 8. Patch team
print("\n[8] PATCH /api/tickets/{id}/assign")
d = api_patch(f"/api/tickets/{new_id}/assign", {"team": "Hydro Maintenance Crew"})
check("Team updated", d["assigned_team"] == "Hydro Maintenance Crew", d.get("assigned_team"))

# 9. Filter by asset_type
print("\n[9] GET /api/tickets?asset_type=wind")
d = api_get("/api/tickets?asset_type=wind")
check("Wind filter returns results", d["total"] >= 1, f"total={d['total']}")
if d["tickets"]:
    check("All results are wind assets", all(t["asset_type"].lower() == "wind" for t in d["tickets"]))

# 10. Filter by severity
print("\n[10] GET /api/tickets?severity=critical")
d = api_get("/api/tickets?severity=critical")
check("Critical filter returns results", d["total"] >= 1, f"total={d['total']}")

# 11. Filter by status
print("\n[11] GET /api/tickets?status=in_progress")
d = api_get("/api/tickets?status=in_progress")
check("In-progress filter returns results", d["total"] >= 1, f"total={d['total']}")

# 12. Metrics
print("\n[12] GET /api/metrics")
d = api_get("/api/metrics")
check("Has total_tickets", "total_tickets" in d)
check("Has severity_distribution", "severity_distribution" in d)
check("Has category_distribution", "category_distribution" in d)
check("Has team_workload", "team_workload" in d)

# 13. Evaluation
print("\n[13] GET /api/evaluation")
d = api_get("/api/evaluation")
check(f"Labeled examples >= 6 (got {d.get('total_labeled_examples')})", d.get("total_labeled_examples", 0) >= 6)
check("Has category_accuracy", "category_accuracy" in d)
check("Has confusion_matrix", "confusion_matrix" in d)

# 14. Delete the test ticket
print("\n[14] DELETE /api/tickets/{id}")
d = api_delete(f"/api/tickets/{new_id}")
check("Delete successful", d.get("message") == "Ticket deleted successfully.")

# Verify deleted
print("\n[15] GET /api/tickets/{id} (should 404)")
try:
    api_get(f"/api/tickets/{new_id}")
    check("Returns 404 after delete", False, "Got 200 instead of 404")
except urllib.error.HTTPError as e:
    check("Returns 404 after delete", e.code == 404, f"Got {e.code}")

# 16. Frontend serves
print("\n[16] GET / (frontend)")
try:
    r = urllib.request.urlopen(f"{BASE}/")
    html = r.read().decode()
    check("Frontend HTML served", "<html" in html.lower() or "<!doctype" in html.lower())
except Exception as e:
    check("Frontend HTML served", False, str(e))

# 17. Health check endpoint
print("\n[17] GET /api/health")
try:
    h = api_get("/api/health")
    check("Health status healthy", h.get("status") == "healthy")
    check("Database connected", h.get("database") == "connected")
except Exception as e:
    check("Health check failed", False, str(e))

# Summary
print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
print("=" * 60)
if __name__ == "__main__":
    sys.exit(1 if failed else 0)

