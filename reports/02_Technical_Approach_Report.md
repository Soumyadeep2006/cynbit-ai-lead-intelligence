# Technical Approach Report
## Cynbit AI — Intelligent Lead Qualification & Project Discovery Agent

## 1. Objective and scope

Build a demonstrable web prototype that accepts a B2B project inquiry and returns a structured discovery brief. Cynbit's public contact page already invites project inquiries and says requirements are analyzed before a tailored strategic overview is prepared. The MVP explores how AI could assist that discovery step; it does not claim access to Cynbit's internal workflow and does not connect to production systems.

Public references:
- https://www.cynbit.in/services
- https://www.cynbit.in/contact
- https://www.cynbit.in/careers/ai-ml-engineer-intern

## 2. Technology choices

| Component | Choice | Rationale |
|---|---|---|
| UI | Streamlit | Fast, readable interactive Python prototype |
| Language | Python | Suitable for text processing and AI integration |
| Baseline | Transparent rules and keyword taxonomy | Works without credentials; easy to inspect |
| Optional LLM | Google Gemini through `google-genai` | Natural-language synthesis into a constrained JSON schema |
| Output | JSON download | Simple handoff format for future CRM/API integration |

## 3. System architecture

```text
User / Project Inquiry
        |
        v
Streamlit Intake Form
        |
        v
Input Validation & Normalization
        |
        +-------------------------------+
        |                               |
        v                               v
Rule-based Baseline              Optional Gemini LLM
        |                         (API key configured)
        +---------------+---------------+
                        |
                        v
              Structured Qualification
       (service, priority, gaps, questions, next step)
                        |
                        v
             Human Review + JSON Export
```

## 4. Data flow

The form captures contact name, business email, company, role, problem statement, expected users/volume, current systems, budget range, and target timeline. The application packages these fields into a dictionary. The selected analysis engine generates a structured result. The UI displays the result and permits JSON export.

The prototype does not persist inquiry records to a database. It does not send data to Cynbit. If Gemini is enabled, the inquiry content is sent to the configured Gemini API; users should use synthetic or approved non-sensitive data only.

## 5. Model and prompt strategy

The deterministic baseline uses keyword matching against an illustrative service taxonomy and checks whether important qualification fields are missing. Its priority score is a simple heuristic for demonstration, not a trained model or validated business score.

When a Gemini API key is available, the optional LLM path requests JSON with a fixed schema. The prompt instructs the model not to invent facts and to state uncertainty. JSON parsing failures or API errors fall back to the baseline.

A production version should validate the output against a formal schema, retain prompt/model versions, test prompt injection resistance, and evaluate the model on a representative reviewed dataset.

## 6. Evaluation plan

Create a consented and anonymized evaluation set of representative inquiries. Have domain reviewers label the expected service category, required missing fields, and appropriate next action. Evaluate:
- Service-category macro F1 and confusion matrix.
- Missing-field precision and recall.
- Human acceptance/correction rate for discovery questions.
- Median time to prepare a usable brief.
- LLM JSON validity and unsupported-claim rate.

Compare the LLM approach with the rule-based baseline. Do not claim predictive accuracy until measured on held-out examples.

## 7. Security, privacy, and responsible AI

- Do not collect unnecessary personal or sensitive data.
- Keep API keys in environment variables or Streamlit secrets; never commit them.
- Use synthetic inquiries for public demos.
- Require human review before routing or contacting a lead.
- Never automatically reject or rank people based on protected or sensitive traits.
- Add authentication, authorization, audit logs, encryption, retention controls, and consent review before production use.

## 8. Run and deployment

Install dependencies with `pip install -r requirements.txt`, then run `streamlit run app.py`. Optional Gemini access is configured through `GEMINI_API_KEY`. The app remains usable in baseline mode without an API key.

## 9. Future roadmap

1. Validate service taxonomy with Cynbit.
2. Add structured output schema validation and automated tests.
3. Add CRM sandbox integration with explicit approval.
4. Build a reviewed evaluation dataset and compare baseline vs. LLM.
5. Add secure authentication, monitoring, audit trails, and deployment.
6. Consider retrieval-augmented generation over approved service documentation if it improves factual service matching.
