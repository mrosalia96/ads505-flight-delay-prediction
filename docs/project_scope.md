# Project scope and decision framing

Working notes for the technical notebook and executive deliverables. Business language here should match the brief and slides.

## Business problem

Airlines and airports learn about many delays only as they unfold. A pre-departure risk score for flights leaving major West Coast / Mountain hubs could help operations leaders focus attention before a bank of departures slips.

## Chief stakeholder (working assumption)

**Director of Airport Operations / Airline Station Operations** for a multi-airport network that includes SAN (with LAX, PHX, DEN, and SEA as peer hubs in the sample).

## Decision the model supports

Intended use: a **same-day watch list** refreshed before each busy departure window. For each scheduled departure, flag **elevated delay risk** (≥ 15 minutes past scheduled departure) so the stakeholder can:

- Pre-position gate / ramp staffing
- Adjust turnaround buffers on high-risk turns
- Trigger earlier passenger communication

Exact operational playbook is outside the data; the model informs **where to look first**, not automated cancellations.

## Cost asymmetry (working assumption)

| Error | Business meaning | Relative cost (hypothesis) |
|-------|------------------|----------------------------|
| False positive | Flag a flight that leaves on time | Wasted attention / mild overstaffing |
| False negative | Miss a flight that delays ≥ 15 min | Missed chance to staff, buffer, or warn passengers; higher passenger and network cost |

**Implication:** Prefer models and thresholds that reduce costly misses (false negatives) when trade-offs appear, and report precision/recall (or cost-weighted metrics) against a simple baseline (e.g., always predict majority class, or a rules baseline using historical delay rate by airport/hour).

These assumptions are carried into the business brief without airline-specific dollar costs (proprietary). Evaluation emphasizes recall under a usable flag-rate cap versus do-nothing and random baselines.

## In scope

- Public BTS on-time fields known before departure (schedule, route, carrier, time-of-day, etc.)
- Public weather near origin at/before departure
- Train / validation / test split that respects time
- Comparison of a small set of interpretable and stronger models
- Business-framed evaluation vs baseline

## Out of scope (course / v1)

- Full U.S. national archive
- Real-time streaming deployment
- Causal claims about weather vs operations
- Using post-delay cause codes as predictive features
- Passenger-level or airline proprietary cost systems

## Success for this course project

1. Reproducible notebook + GitHub README documenting setup and sources  
2. Clear Model Brief for a technical peer  
3. Executive brief / slides / video with one justified recommendation aligned to the notebook  

## Team

Team 4 — Michael Rosalia (solo, instructor-approved). All contributions by Michael Rosalia.
