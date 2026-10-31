# AI Opportunity Report
## Cynbit AI — Intelligent Lead Qualification & Project Discovery Agent

**Prepared for:** Cynbit AI/ML Engineer Intern — Technical Role Assessment  
**Prepared by:** Candidate  
**Date:** 31 October 2026

## 1. Executive summary

This report proposes an AI-assisted inquiry qualification workflow for a technology services business. The system converts unstructured project inquiries into a structured discovery brief: likely service category, priority suggestion, missing requirements, follow-up questions, and a recommended human next step.

The proposal is based on Cynbit's publicly presented AI and software service positioning. It is a hypothesis to validate with the Cynbit team, not a statement that Cynbit currently has this operational problem.

## 2. Public-surface observations and business opportunity

Cynbit's public website describes autonomous agents for lead coordination, LLM automation for manual data entry and document handling, AI voice agents, and CRM automation. Its contact page already presents a project inquiry workflow and says the team will analyze requirements and prepare a tailored strategic overview before connecting. This makes an AI-assisted discovery brief a directly relevant extension to an existing public-facing workflow—not an assumption that Cynbit lacks an intake process.

Public references reviewed:
- Cynbit Services: https://www.cynbit.in/services
- Cynbit Contact / Inquiry Hub: https://www.cynbit.in/contact
- AI/ML Engineer Intern role: https://www.cynbit.in/careers/ai-ml-engineer-intern

The opportunity hypothesis is that project inquiries can vary in completeness and technical specificity. A human team may need to identify the requested capability, clarify scope, understand urgency, and route the inquiry to an appropriate specialist. An AI-assisted intake layer could prepare a first-pass discovery brief for human review.

An AI-assisted intake layer could:
- Standardize the information captured from inquiries.
- Suggest a likely service line for human review.
- Highlight missing scope, budget, timeline, users, and integration details.
- Draft relevant discovery questions.
- Produce a consistent handoff brief for sales or engineering.

## 3. Proposed solution

**Cynbit AI Lead Intelligence & Project Discovery Agent**

### Workflow
1. Receive a project inquiry and basic qualification fields.
2. Extract the problem statement, expected users/volume, systems, budget, and timeline.
3. Recommend a likely service category from an explicitly defined taxonomy.
4. Suggest a priority level with transparent rationale and uncertainty.
5. Identify missing information and generate discovery questions.
6. Export a structured brief for a human team member to review.

### Initial service taxonomy
- AI agents and workflow automation
- Generative AI / LLM applications
- Voice AI
- CRM and lead management
- Document intelligence
- Custom software and cloud integration

These categories are an initial prototype taxonomy and should be checked against Cynbit's current service catalogue.

## 4. Expected business value and success metrics

The prototype does not claim measured business impact. A pilot should establish a baseline and compare:

| Metric | How to measure |
|---|---|
| Time to prepare an inquiry brief | Median minutes per inquiry before vs. after |
| Completeness of first discovery | Required-field completion rate |
| Routing quality | Human-confirmed correct service category |
| Follow-up efficiency | Number of clarification cycles |
| Recommendation quality | Reviewer acceptance and correction rate |

Pilot targets should be agreed with the business after collecting baseline data, rather than invented in advance.

## 5. Feasibility and data requirements

A first version can operate on inquiry form text and a small service taxonomy. A production-grade system would require:
- Approved service catalogue and routing rules.
- Historical inquiries with consent and appropriate access controls.
- Human-reviewed service labels and outcomes, if predictive modelling is later considered.
- CRM fields and workflow integration requirements.
- Clear data retention and privacy rules.

No historical Cynbit data was available for this assessment, so the proof of concept uses synthetic demonstration inputs.

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Incorrect service recommendation | Human review and editable taxonomy |
| LLM hallucination | Constrained JSON output, evidence from supplied text only, fallback baseline |
| Biased or misleading priority score | Treat as triage hint; expose rationale; never auto-reject |
| Sensitive data exposure | Minimize input, avoid sensitive data, secure API secrets |
| Poor performance on real inquiries | Pilot evaluation and iterative error analysis |

## 7. Recommendation

Run a small, human-in-the-loop pilot on approved, anonymized inquiries. First validate the taxonomy and workflow with sales/engineering stakeholders. Only consider a trained lead-scoring model after enough representative, quality-labelled data exists. The immediate value is structured discovery and consistent handoff, not automated decision-making.
