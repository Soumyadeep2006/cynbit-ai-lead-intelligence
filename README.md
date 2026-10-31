# Cynbit AI — Lead Intelligence & Project Discovery Agent

A focused proof of concept for the Cynbit AI/ML Engineer Intern assessment. It turns an inbound project inquiry into a structured discovery brief: service-line recommendation, lead-priority suggestion, missing information, discovery questions, and a next-best action.

## Why this use case

Cynbit publicly positions itself around AI/software services and business automation. A structured intake assistant is a plausible fit for a services business receiving project inquiries: it can improve consistency of discovery, reduce manual triage, and help a human team respond with the right questions. This is a proposed opportunity, not a claim about Cynbit's internal systems or current pain points.

## Features

- Streamlit UI for entering a realistic B2B inquiry.
- Rule-based baseline works without an API key.
- Optional Gemini LLM analysis when configured.
- Structured JSON discovery brief export.
- Missing-information detection and human-review safeguards.
- No automatic rejection or autonomous customer contact.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Optional Gemini setup

Set an API key in the terminal before starting the app:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
$env:GEMINI_MODEL="gemini-2.5-flash"
streamlit run app.py
```

Or create `.streamlit/secrets.toml` (never commit this file):

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

Without a key, the app automatically uses the rule-based baseline. The selected engine is shown in the UI.

## Test scenario

Company: Northstar Support  
Problem: "We receive around 300 support tickets daily and want an AI assistant that can answer questions from internal policy documents, create draft replies, and escalate complex tickets to a human."  
Users/volume: "15 support agents, 300 tickets/day"  
Systems: "Website, Google Drive, existing ticketing tool"  
Budget: "₹2–10 lakh"  
Timeline: "1–2 months"

Expected behavior: likely recommend Generative AI / LLM or Document Intelligence depending on signals; show discovery questions, missing details, and a human-led next step. The exact result may differ between baseline and LLM.

## Architecture

1. **Input layer:** contact and project context entered in Streamlit.
2. **Analysis layer:** Gemini structured analysis if configured; otherwise deterministic keyword/completeness baseline.
3. **Output layer:** service recommendation, priority suggestion, uncertainty, missing fields, discovery questions.
4. **Export layer:** downloadable JSON discovery brief.
5. **Human review:** team member validates fit and decides next action.

## Limitations and next steps

- Current service taxonomy and keyword rules are illustrative and should be validated with Cynbit.
- No CRM integration, persistent database, authentication, or production deployment.
- Priority scoring is a prototype heuristic, not a trained predictive model.
- For production: evaluate on consented historical inquiry data; define labels with sales experts; measure precision/recall and calibration; add audit logs, access controls, retention policy, CRM integration, and human approval.

## Responsible use

Do not enter confidential customer data or sensitive personal information. Do not use the score as the sole basis for accepting, rejecting, or deprioritizing a customer. All recommendations require human review.
