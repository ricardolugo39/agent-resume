# Resume Agent — Project Status
**Last Updated:** 2026-06-30

---

# North Star

Increase interview rate by generating truthful, highly targeted resumes that maximize interview probability.

The product is **not** judged by resume quality alone.

Success metric:

> More recruiter callbacks and interviews.

---

# Current Status

**Sprint 3: MVP — COMPLETE ✅**

The end-to-end pipeline is operational and produces resumes that are considered submission-ready for real applications.

The product is now ready to begin validating against real job applications.

---

# Current Workflow

```text
Job Description
        │
        ▼
Candidate Fit
        │
        ▼
Resume Strategy
        │
        ▼
Achievement Matching
        │
        ▼
Resume Generator
    ├── Summary Writer
    ├── Company Section Writer
    └── Bullet Writer
        │
        ▼
Resume Quality Gate (RQS)
        │
        ├── PASS
        │       │
        │       ▼
        │   Save Resume
        │
        └── PASS_WITH_WARNINGS / FAIL
                │
                ▼
          Rewrite Plan
                │
                ▼
      Single Guided Rewrite
                │
                ▼
      Final Quality Gate
                │
                ▼
          Save Resume
```

---

# Completed

## Candidate Fit
- ✅ Candidate fit evaluation
- ✅ Interview probability
- ✅ Proven matches
- ✅ Credible adjacencies
- ✅ Hard gaps
- ✅ Recruiter concerns
- ✅ Hiring manager concerns

---

## Resume Strategy

- ✅ Target positioning
- ✅ Winning story
- ✅ Primary angle
- ✅ Secondary angle
- ✅ Resume narrative
- ✅ Role dimensions
- ✅ Selection priorities

---

## Achievement Matching

- ✅ Strategy-aware matching
- ✅ Evidence selection
- ✅ Prioritized achievements

---

## Resume Generation

### Summary

- ✅ Strategy-aware
- ✅ Evidence-first
- ✅ Credibility guardrails
- ✅ Avoid overclaiming

### Company Sections

- ✅ Strategy-aware
- ✅ Cohesive experience sections
- ✅ Human-style writing
- ✅ Evidence grounded

### Bullet Rewriter

- ✅ Uses Resume Strategy
- ✅ Uses Rewrite Plan
- ✅ Uses evidence maturity
- ✅ Prevents hallucinations

---

## Resume Quality Gate

Implemented RQS evaluation.

Current behavior:

- ✅ Evaluates execution only
- ✅ Does NOT re-run Candidate Fit
- ✅ Does NOT require mentioning capability gaps
- ✅ Produces strengths
- ✅ Produces findings
- ✅ Produces Rewrite Plan
- ✅ Produces rewrite prompt
- ✅ Uses interview probability philosophy

---

## Rewrite System

Implemented one-pass rewrite architecture.

Flow:

```
Draft Resume

↓

Quality Gate

↓

Rewrite Plan

↓

Rewrite Resume

↓

Final Quality Gate
```

No recursive optimization.

No endless loops.

---

## Resume Persistence

Every generated resume is automatically stored.

Current database:

`data/resume_agent.sqlite`

Stored:

- Resume ID
- Job Description
- Candidate Fit
- Resume Strategy
- Resume Outline
- Quality Gate
- Candidate Fit Score
- Quality Score
- Status
- Timestamp

Current status values:

- Generated
- Applied
- Recruiter Contacted
- Interview
- Rejected
- Offer
- Withdrawn

Example Resume ID:

```
RES-20260630-001
```

This creates the foundation for tracking interview performance over time.

---

# MVP Decision

**MVP APPROVED**

The generated resumes are considered good enough to begin applying for real Product Manager positions.

Future improvements should be driven by actual hiring outcomes rather than additional architecture.

---

# Backlog

## Resume Quality

- Improve summary wording for stronger executive impact.
- Reduce occasional repetitive metrics.
- Better control bullet count per company.
- Improve skills section selection.

---

## Resume Generator

- Better variation in sentence openings.
- Smarter bullet length balancing.
- Improve company section cohesion.

---

## Quality Gate

- Continue calibration using real resumes.
- Improve scoring consistency.
- Reduce unnecessary PASS_WITH_WARNINGS.
- Improve rewrite guidance precision.

---

## Application Tracking

Planned enhancements:

- Company auto-extraction
- Job title auto-extraction
- Job URL
- Recruiter name
- Recruiter email
- Interview dates
- Follow-up tracking
- Outcome analytics

---

# Next Sprint

## Sprint 4 — Real Application Validation

Goal:

Validate Resume Agent using real job applications.

Focus:

- Apply to real jobs.
- Track every application.
- Record recruiter responses.
- Measure interview conversion.
- Improve resume generation using real-world outcomes.

Success criteria:

- Submit multiple real applications.
- Store every generated resume.
- Track interview rate.
- Use recruiter feedback to prioritize future improvements.

No new major architecture unless directly supported by application results.