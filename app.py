import json
import os
import re
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Cynbit AI | Lead Intelligence", page_icon="🤖", layout="wide")

SERVICES = {
    "AI Agents & Automation": ["agent", "automation", "workflow", "autonomous", "process"],
    "Generative AI / LLM": ["llm", "generative ai", "chatbot", "rag", "knowledge assistant", "prompt"],
    "Voice AI": ["voice", "call", "ivr", "speech", "phone agent"],
    "CRM & Lead Management": ["crm", "lead", "sales pipeline", "customer management", "qualification"],
    "Custom Software / Cloud": ["software", "web app", "application", "cloud", "api", "integration", "dashboard"],
    "Document Intelligence": ["document", "invoice", "pdf", "extract", "ocr", "contract"]
}

def rule_based_analysis(payload: dict) -> dict:
    text = " ".join(str(v) for v in payload.values()).lower()
    problem = str(payload.get("problem", "")).lower()

    # Weighted service classification
    scores = {
        service: sum(1 for term in terms if term in text)
        for service, terms in SERVICES.items()
    }

    # Give stronger weight to the actual business problem
    if any(term in problem for term in [
        "rag", "retrieval-augmented generation",
        "knowledge base", "internal documents",
        "customer support assistant", "chatbot",
        "llm", "generative ai"
    ]):
        scores["Generative AI / LLM"] += 6

    if any(term in problem for term in [
        "document extraction", "pdf processing",
        "invoice extraction", "ocr"
    ]):
        scores["Document Intelligence"] += 5

    if any(term in problem for term in [
        "autonomous agent", "multi-agent",
        "agentic workflow", "workflow automation"
    ]):
        scores["AI Agents & Automation"] += 5

    if any(term in problem for term in [
        "voice assistant", "voice agent",
        "speech recognition", "phone calls"
    ]):
        scores["Voice AI"] += 5

    if any(term in problem for term in [
        "crm integration", "sales pipeline",
        "lead management"
    ]):
        scores["CRM & Lead Management"] += 5

    service = max(scores, key=scores.get)

    # Qualification assessment
    budget = str(payload.get("budget", "")).lower()
    timeline = str(payload.get("timeline", "")).lower()

    urgency = (
        "High" if any(x in timeline for x in
        ["asap", "1 week", "2 weeks", "urgent"])
        else "Medium"
    )

    if any(x in budget for x in [
        "above", "₹10", "10 lakh", "enterprise"
    ]):
        commercial_fit = "High"
    elif any(x in budget for x in [
        "not sure", "discuss", "flexible", "medium",
        "2 lakh", "2–10 lakh", "2-10 lakh"
    ]):
        commercial_fit = "Medium"
    else:
        commercial_fit = "Not established"

    missing = []
    required_fields = {
        "problem": "specific business problem",
        "users": "expected users or volume",
        "budget": "budget range",
        "timeline": "target timeline",
        "systems": "existing tools / systems"
    }

    for key, label in required_fields.items():
        value_entered = str(payload.get(key, "")).strip()
        if not value_entered or value_entered.lower() in [
            "not sure", "not specified"
        ]:
            missing.append(label)

    score = 25
    score += 15 if urgency == "High" else 8
    score += 20 if commercial_fit == "High" else 12 if commercial_fit == "Medium" else 0
    score += 15 if payload.get("email") else 0
    score += 15 if payload.get("company") else 0

    priority_score = min(100, score)

    return {
        "recommended_service": service,
        "lead_priority": (
            "High" if priority_score >= 70
            else "Medium" if priority_score >= 50
            else "Low"
        ),
        "priority_score": priority_score,
        "urgency": urgency,
        "estimated_commercial_fit": commercial_fit,
        "problem_summary": payload.get(
            "problem", "No problem statement supplied."
        ),
        "recommended_next_step": (
            "Schedule a 20-minute discovery call to validate "
            "scope, success metrics, budget, and integration requirements."
        ),
        "missing_information": missing,
        "discovery_questions": [
            "What measurable business outcome defines success?",
            "Which systems and data sources require integration?",
            "Who will use the solution and what is the expected volume?",
            "What are the target launch date and budget?"
        ],
        "reasoning": (
            "Classification uses weighted keyword signals. "
            "Priority is a prototype heuristic, not a validated "
            "prediction of customer value. Human review is required."
        )
    }


def gemini_analysis(payload: dict):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""
    api_key = api_key or os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        prompt = f"""You are a careful B2B solution-discovery assistant for Cynbit, an AI and software services company.
Analyze this inbound project inquiry. Do not invent facts. Return ONLY valid JSON with keys:
recommended_service, lead_priority (High/Medium/Low), priority_score (0-100), urgency,
estimated_commercial_fit, problem_summary, recommended_next_step, missing_information (array),
discovery_questions (array of 3-5), reasoning.
Be cautious: never infer budget or urgency unless supplied. Explain uncertainty.
Inquiry: {json.dumps(payload, ensure_ascii=False)}"""
        response = client.models.generate_content(model=model, contents=prompt)
        raw = response.text.strip()
        raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
        return json.loads(raw)
    except Exception as exc:
        st.warning(f"LLM call unavailable; showing baseline analysis instead. Details: {exc}")
        return None

st.title("🤖 Cynbit AI — Lead Intelligence & Project Discovery")
st.caption("Assessment proof of concept | Inbound inquiry → structured qualification → next-best action")
with st.sidebar:
    st.header("Analysis settings")
    use_llm = st.toggle("Use Gemini LLM when configured", value=True)
    st.caption("Without GEMINI_API_KEY, the app uses a transparent rule-based baseline.")
    st.divider()
    st.markdown("**Prototype safeguards**")
    st.write("• Human review required")
    st.write("• No automatic rejection")
    st.write("• Do not enter sensitive personal data")

left, right = st.columns([1.05, 1])
with left:
    st.subheader("1. Customer inquiry")
    with st.form("lead_form"):
        name = st.text_input("Contact name")
        email = st.text_input("Business email")
        company = st.text_input("Company")
        role = st.text_input("Role / department")
        problem = st.text_area("What are you trying to achieve?", height=150,
            placeholder="Example: We receive 300 support requests per day and want an AI assistant that can answer from our internal documentation and escalate complex cases.")
        users = st.text_input("Expected users / volume", placeholder="e.g. 20 agents, 300 tickets/day")
        systems = st.text_input("Existing tools / systems", placeholder="e.g. HubSpot, website, Google Drive, ERP")
        budget = st.selectbox("Budget range", ["Not specified", "Under ₹50,000", "₹50,000–₹2 lakh", "₹2–10 lakh", "Above ₹10 lakh", "Flexible / discuss"])
        timeline = st.selectbox("Target timeline", ["Not specified", "ASAP / within 2 weeks", "1–2 months", "3–6 months", "More than 6 months"])
        submitted = st.form_submit_button("Analyze inquiry", type="primary", use_container_width=True)

if submitted:
    inquiry = {"name": name, "email": email, "company": company, "role": role, "problem": problem,
               "users": users, "systems": systems, "budget": budget, "timeline": timeline}
    if not problem.strip():
        st.error("Please describe the business problem before running the analysis.")
    else:
        result = gemini_analysis(inquiry) if use_llm else None
        engine = "Gemini LLM" if result else "Rule-based baseline"
        result = result or rule_based_analysis(inquiry)
        st.session_state["analysis"] = {"inquiry": inquiry, "result": result, "engine": engine}
        st.session_state["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with right:
    st.subheader("2. Qualification output")
    if "analysis" not in st.session_state:
        st.info("Complete the inquiry form and select **Analyze inquiry** to see the qualification report.")
        st.markdown("**What this prototype demonstrates**")
        st.markdown("- Service-line recommendation\n- Lead priority and rationale\n- Missing-information detection\n- Discovery questions\n- Suggested next action")
    else:
        item = st.session_state["analysis"]
        r = item["result"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Lead priority", str(r.get("lead_priority", "Review")))
        c2.metric("Priority score", f'{r.get("priority_score", "—")}/100')
        c3.metric("Analysis engine", item["engine"])
        st.success(f'Recommended service: **{r.get("recommended_service", "Needs review")}**')
        st.markdown("**Problem summary**")
        st.write(r.get("problem_summary", "—"))
        st.markdown("**Recommended next step**")
        st.write(r.get("recommended_next_step", "—"))
        st.markdown("**Missing information**")
        missing = r.get("missing_information", [])
        st.write(", ".join(missing) if missing else "No major gaps detected from supplied fields.")
        st.markdown("**Discovery questions**")
        for q in r.get("discovery_questions", []):
            st.markdown(f"- {q}")
        with st.expander("Reasoning and full structured result"):
            st.write(r.get("reasoning", ""))
            st.json(r)
        export = {"created_at": st.session_state.get("created_at"), "engine": item["engine"], "inquiry": item["inquiry"], "analysis": r}
        st.download_button("Download discovery brief (JSON)", json.dumps(export, indent=2, ensure_ascii=False),
                           file_name="cynbit_lead_discovery_brief.json", mime="application/json")
        st.caption("Decision-support only. A Cynbit team member must verify the recommendation before contacting or prioritizing a lead.")

st.divider()
st.caption("Cynbit AI assessment prototype • Demonstration data only • No data is sent to Cynbit.")
