import math
import re

from datetime import datetime, timezone

from typing import List, Dict, Any, Tuple, Optional



from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity



from backend.config import DATASET_PATH

from backend.data.dataset_loader import load_dataset

from backend.schemas import (

    TicketAnalysisRequest,

    TicketAnalysisResponse,

    PriorityBreakdown,

    HistoricalMatch,

)



# Domain Taxonomy & Mapping

CATEGORY_META = {

    "inverter_thermal": {

        "label": "Inverter Thermal & Electrical Faults",

        "keywords": ["inverter", "tripping", "thermal", "igbt", "temperature", "overheating", "alarm", "cooling", "heat"],

        "root_cause": "Thermal stress, fan failure, or IGBT over-temperature condition causing automatic inverter trip.",

        "action": "Inspect inverter cooling fans/air filters, test IGBT thermal paste, and log temperature telemetry.",

        "team": "Solar & Electrical Ops",

        "base_severity": "high"

    },

    "gearbox_vibration": {

        "label": "Turbine Gearbox & Mechanical Vibration",

        "keywords": ["gearbox", "vibration", "bearing", "noise", "abnormal", "mechanical", "shaft", "lubrication"],

        "root_cause": "Bearing mechanical wear, main shaft misalignment, or lube oil pressure degradation.",

        "action": "Schedule urgent vibration spectrum analysis, inspect lube oil filter for metallic debris, and limit turbine output.",

        "team": "Wind Mechanical Maintenance",

        "base_severity": "critical"

    },

    "inspection_compliance": {

        "label": "Safety & Compliance Inspection",

        "keywords": ["inspection", "checklist", "spillway", "gate", "compliance", "pending", "audit", "dam", "regulatory"],

        "root_cause": "Pending statutory compliance inspection or scheduled preventive maintenance interval reached.",

        "action": "Execute spillway hydraulic gate checklist, log safety inspection logs, and update regulatory register.",

        "team": "EHS & Hydro Safety Team",

        "base_severity": "medium"

    },

    "data_gap": {

        "label": "SCADA Telemetry & Communication Gap",

        "keywords": ["scada", "missing", "telemetry", "communication", "offline", "data gap", "modbus", "rtu", "gateway"],

        "root_cause": "SCADA network gateway timeout, RTU transceiver failure, or local communication link disconnect.",

        "action": "Check RTU module power supply, restart network switch, and verify Modbus telemetry data stream.",

        "team": "SCADA & Telemetry Team",

        "base_severity": "medium"

    },

    "pitch_system": {

        "label": "Blade Pitch & Aerodynamic Control",

        "keywords": ["pitch", "blade", "gust", "wind gust", "encoder", "hydraulic pitch", "feathering"],

        "root_cause": "Blade pitch encoder discrepancy or hydraulic pitch cylinder pressure drop following extreme wind gust.",

        "action": "Calibrate pitch cylinder encoder, test hydraulic accumulator pressure, and run pitch emergency feather test.",

        "team": "Wind Turbine Specialists",

        "base_severity": "high"

    },

    "grid_curtailment": {

        "label": "Grid Dispatch & Curtailment Alignment",

        "keywords": ["curtailment", "grid", "sldc", "generation", "dashboard", "ramp", "power plant controller", "ppc"],

        "root_cause": "SLDC grid curtailment dispatch mismatch or automated Power Plant Controller (PPC) setpoint sync latency.",

        "action": "Cross-check active power setpoint with SLDC dispatcher, adjust PPC ramp rate, and log generation loss.",

        "team": "Grid & SLDC Dispatch Ops",

        "base_severity": "medium"

    },

    "transformer_substation": {

        "label": "Substation & Transformer Maintenance",

        "keywords": ["transformer", "substation", "oil leak", "buchholz", "bushing", "breaker", "switchyard", "sf6"],

        "root_cause": "Transformer oil degradation, insulation breakdown, or gas accumulation in Buchholz relay.",

        "action": "Perform Dissolved Gas Analysis (DGA), check oil level gauge, and inspect switchyard breaker status.",

        "team": "High Voltage Substation Team",

        "base_severity": "high"

    },

    "battery_bms": {

        "label": "BMS & Energy Storage System",

        "keywords": ["battery", "bms", "cell", "soc", "bess", "rack", "voltage imbalance"],

        "root_cause": "Battery cell voltage imbalance or thermal management HVAC system fault in BESS container.",

        "action": "Isolate affected battery rack, run automated cell balancing cycle, and check HVAC container cooling.",

        "team": "BESS & Energy Storage Team",

        "base_severity": "high"

    },

    "general_maintenance": {

        "label": "General Operations & Maintenance",

        "keywords": ["general", "routine", "cleaning", "physical", "door", "light", "fence"],

        "root_cause": "Routine operational wear or facility site maintenance requirement.",

        "action": "Assign site technician for physical walkthrough inspection and maintenance routine execution.",

        "team": "General Operations Team",

        "base_severity": "low"

    }

}



SAFETY_KEYWORDS = [

    "fire", "smoke", "explosion", "overheating", "tripping repeatedly", "oil leak",

    "vibration increased", "critical", "abnormal noise", "high voltage", "arc flash",

    "spillway gate", "uncontrolled"

]



SEVERITY_BASE_SCORES = {

    "critical": 85.0,

    "high": 65.0,

    "medium": 45.0,

    "low": 25.0

}



class TicketPrioritizationAgent:

    def __init__(self, dataset_path=DATASET_PATH):

        self.dataset_path = dataset_path

        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

        self.benchmark_data = []

        self.tfidf_matrix = None

        self._initialize_model()



    def _initialize_model(self):

        """Load benchmark dataset and fit TF-IDF vectorizer for RAG lookup."""

        # Load dataset as list of dicts
        self.benchmark_data = load_dataset(self.dataset_path)
        if self.benchmark_data:
            # Extract descriptions for TF-IDF fitting
            descriptions = [row.get("description", "") for row in self.benchmark_data]
            self.tfidf_matrix = self.vectorizer.fit_transform(descriptions)



    def reload_dataset(self):

        """Re-fit TF-IDF if dataset changes."""

        self._initialize_model()



    def find_similar_tickets(self, query_text: str, top_k: int = 3) -> List[HistoricalMatch]:

        """RAG lookup: return top matching historical tickets based on TF-IDF Cosine Similarity."""

        if not self.benchmark_data or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]
        matches = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.01:
                row = self.benchmark_data[idx]
                matches.append(
                    HistoricalMatch(
                        ticket_id=str(row.get("ticket_id", f"HIST-{idx}")),
                        asset_type=str(row.get("asset_type", "unknown")),
                        description=str(row.get("description", "")),
                        target_severity=str(row.get("target_severity", "medium")),
                        target_category=str(row.get("target_category", "general_maintenance")),
                        similarity_score=round(score, 4)
                    )
                )
        return matches



    def predict_category(self, text: str, asset_type: Optional[str] = None) -> Tuple[str, str]:

        """Classify ticket into category using keyword matching + TF-IDF similarity to benchmark data."""

        text_lower = text.lower()

        scores: Dict[str, float] = {cat: 0.0 for cat in CATEGORY_META}



        # 1. Keyword scoring

        for cat, meta in CATEGORY_META.items():

            for kw in meta["keywords"]:

                if kw in text_lower:

                    scores[cat] += 2.5



        # Asset type bonus

        if asset_type:

            asset_lower = asset_type.lower()

            if "solar" in asset_lower:

                scores["inverter_thermal"] += 1.0

                scores["data_gap"] += 0.5

            elif "wind" in asset_lower:

                scores["gearbox_vibration"] += 1.0

                scores["pitch_system"] += 1.0

            elif "hydro" in asset_lower:

                scores["inspection_compliance"] += 1.5

            elif "grid" in asset_lower or "substation" in asset_lower:

                scores["grid_curtailment"] += 1.0

                scores["transformer_substation"] += 1.0

            elif "battery" in asset_lower or "bess" in asset_lower or "storage" in asset_lower:

                scores["battery_bms"] += 1.5



        # 2. Similarity with benchmark labeled samples

        matches = self.find_similar_tickets(text, top_k=3)

        for match in matches:

            if match.target_category in scores:

                scores[match.target_category] += match.similarity_score * 3.0



        # Pick best category

        best_category = max(scores.items(), key=lambda x: x[1])[0]

        if scores[best_category] == 0:

            best_category = "general_maintenance"



        return best_category, CATEGORY_META[best_category]["label"]



    def determine_severity_and_priority(

        self, text: str, category: str, asset_type: Optional[str] = None

    ) -> Tuple[str, float, str, str, PriorityBreakdown, List[str], bool, Optional[str]]:

        """Calculate severity, priority score (0-100), breakdown, indicators, and safety escalation."""

        text_lower = text.lower()

        modifiers = []

        indicators = []

        safety_escalation = False

        safety_warning = None



        # Base severity from category default

        cat_meta = CATEGORY_META.get(category, CATEGORY_META["general_maintenance"])

        default_sev = cat_meta["base_severity"]



        # Check safety keywords

        matched_safety = [kw for kw in SAFETY_KEYWORDS if kw in text_lower]
        if matched_safety:

            safety_escalation = True

            indicators.extend(matched_safety)

            safety_warning = f"SAFETY ALERT: Critical term(s) identified: {', '.join(matched_safety)}. Mandatory supervisor check required."



        # Determine overall severity level

        if any(term in text_lower for term in ["critical", "vibration has increased", "abnormal noise", "fire", "explosion"]):

            severity = "critical"

        elif safety_escalation or any(term in text_lower for term in ["tripping", "high temperature", "pitch error", "oil leak"]):

            severity = "high"

        elif default_sev in ["high", "critical"] and not any(term in text_lower for term in ["low", "routine"]):

            severity = default_sev

        elif any(term in text_lower for term in ["missing", "pending", "curtailment", "checklist"]):

            severity = "medium"

        else:

            severity = "low"



        base_score = SEVERITY_BASE_SCORES[severity]

        current_score = base_score



        # Modifiers

        if safety_escalation:

            mod = 10.0

            current_score += mod

            modifiers.append(f"Safety Hazard Trigger (+{mod:.1f})")



        if any(term in text_lower for term in ["tripping", "offline", "missing", "error", "curtailment"]):

            mod = 5.0

            current_score += mod

            modifiers.append(f"Operational Disruption Impact (+{mod:.1f})")



        if asset_type:

            asset_lower = asset_type.lower()

            if "grid" in asset_lower or "substation" in asset_lower:

                mod = 4.0

                current_score += mod

                modifiers.append(f"Critical Substation Infrastructure (+{mod:.1f})")

            elif "wind" in asset_lower or "hydro" in asset_lower:

                mod = 3.0

                current_score += mod

                modifiers.append(f"High-Capacity Renewable Asset (+{mod:.1f})")



        if "repeatedly" in text_lower or "increased" in text_lower:

            mod = 4.0

            current_score += mod

            modifiers.append(f"Escalating Fault Pattern (+{mod:.1f})")



        final_score = min(100.0, max(10.0, round(current_score, 1)))



        # Priority Label

        if final_score >= 80.0:

            priority_label = "CRITICAL"

        elif final_score >= 60.0:

            priority_label = "HIGH"

        elif final_score >= 35.0:

            priority_label = "MEDIUM"

        else:

            priority_label = "LOW"



        explanation = (

            f"Ticket assessed as {priority_label} (Score: {final_score}/100) based on base {severity} severity "

            f"with {len(modifiers)} domain risk adjustment(s)."

        )



        breakdown = PriorityBreakdown(

            base_severity_score=base_score,

            modifiers=modifiers,

            final_score=final_score

        )



        return (

            severity,

            final_score,

            priority_label,

            explanation,

            breakdown,

            list(set(indicators)),

            safety_escalation,

            safety_warning,

        )



    def analyze_ticket(self, request: TicketAnalysisRequest) -> TicketAnalysisResponse:

        """Full end-to-end agentic triage pipeline for a ticket request."""

        text = request.description

        asset_type = request.asset_type or "Renewable Asset"

        asset_id = request.asset_id or "GENERIC"



        category, category_label = self.predict_category(text, asset_type)

        (

            severity,

            priority_score,

            priority_label,

            priority_explanation,

            priority_breakdown,

            indicators,

            safety_escalation,

            safety_warning,

        ) = self.determine_severity_and_priority(text, category, asset_type)



        meta = CATEGORY_META.get(category, CATEGORY_META["general_maintenance"])

        probable_root_cause = meta["root_cause"]

        recommended_action = meta["action"]

        assigned_team = meta["team"]



        similar_tickets = self.find_similar_tickets(text, top_k=3)



        now_str = datetime.now(timezone.utc).isoformat()



        return TicketAnalysisResponse(

            ticket_id=None,

            description=text,

            asset_type=asset_type,

            asset_id=asset_id,

            category=category,

            category_label=category_label,

            severity=severity,

            priority_score=priority_score,

            priority_label=priority_label,

            priority_explanation=priority_explanation,

            priority_breakdown=priority_breakdown,

            indicators=indicators,

            probable_root_cause=probable_root_cause,

            recommended_action=recommended_action,

            assigned_team=assigned_team,

            similar_tickets=similar_tickets,

            safety_escalation=safety_escalation,

            safety_warning=safety_warning,

            human_review_required=safety_escalation or priority_score >= 60.0,

            analysis_method="TF-IDF Cosine Similarity RAG + Domain Rule Triage Engine",

            created_at=now_str,

        )



    def evaluate_benchmark(self) -> Dict[str, Any]:

        """Evaluate agent predictions against bundled maintenance_tickets.csv dataset."""

        data = load_dataset(self.dataset_path)

        if not data:

            return {

                "total_labeled_examples": 0,

                "category_accuracy": 0.0,

                "category_correct": 0,

                "severity_accuracy": 0.0,

                "severity_correct": 0,

                "method": "TF-IDF + Rule-based Agent",

                "limitations": ["No benchmark dataset found."],

                "confusion_matrix": {}

            }



        total = len(data)

        cat_correct = 0

        sev_correct = 0

        matrix = {}



        for row in data:

            text = row.get("description", "")

            asset = row.get("asset_type", "")

            true_cat = row.get("target_category", "")

            true_sev = row.get("target_severity", "")



            pred_cat, _ = self.predict_category(text, asset)

            pred_sev, _, _, _, _, _, _, _ = self.determine_severity_and_priority(text, pred_cat, asset)



            if pred_cat == true_cat:

                cat_correct += 1

            if pred_sev == true_sev:

                sev_correct += 1



            matrix[str(row.get("ticket_id", ""))] = {

                "true_category": true_cat,

                "predicted_category": pred_cat,

                "true_severity": true_sev,

                "predicted_severity": pred_sev,

                "category_match": pred_cat == true_cat,

                "severity_match": pred_sev == true_sev

            }



        cat_acc = round(cat_correct / total, 4) if total > 0 else 0.0

        sev_acc = round(sev_correct / total, 4) if total > 0 else 0.0



        limitations = [

            "Small benchmark evaluation sample size (6 items); model relies on curated energy domain heuristics and TF-IDF.",

            "Edge case descriptions with ambiguous multi-asset fault reports may require LLM fine-tuning.",

            "No real-time SCADA telemetry sensor stream integration in offline benchmark mode."

        ]



        return {

            "total_labeled_examples": total,

            "category_accuracy": cat_acc,

            "category_correct": cat_correct,

            "severity_accuracy": sev_acc,

            "severity_correct": sev_correct,

            "method": "TF-IDF Cosine Similarity Vectorizer + Hybrid Rule-based Expert Agent",

            "limitations": limitations,

            "confusion_matrix": matrix

        }



# Global Agent Instance

agent = TicketPrioritizationAgent()

