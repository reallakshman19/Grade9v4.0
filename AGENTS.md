# AGENTS.md — Instructions for Coding Agents

**Primary specification:** https://github.com/reallakshman19/Grade9v4.0/issues/1

This file applies to all work in this repository.

## Required approach

1. Read Issue #1 in full before creating or editing files. It is the authoritative task specification for the initial implementation.
2. Implement PR slices **in the specified order**. Do not attempt P1/P2 while a prerequisite P0 task is unimplemented.
3. Preserve source field names, stable IDs, canonical cognitive operations, status labels, evidence labels, and B1–B7 terminology. Do not silently rename or merge them.
4. Use Python 3.11+, `jsonschema` and `pytest` as specified. Prefer readable functions with explicit inputs/outputs, simple control flow, and deterministic reports.
5. Before each PR, run `python -m pytest -q`, show the exact output, and add tests for new behavior. A failed or skipped test must be reported, not hidden.
6. Implement fail-closed logic: missing or stale qualification evidence is HOLD; a demonstrably contradictory or invalid assertion is FAIL. Never assume APPROVED.
7. A correct SHA-256, schema validation, page rendering, or matching ID **does not certify scientific or cognitive quality**.
8. Never create human review receipts automatically; only validate externally provided, scoped receipts and their hash/timestamp consistency.
9. Protect provenance. Do not publish source textbook scans, answer-key PDFs, or copyrighted exam papers without appropriate permission. Never claim a synthetic problem is a verified past examination question.
10. Treat directional operations as different until independently accepted: e.g. potential→force differs from force→potential.
11. Never introduce WPE-specific claims into the generic Physics/QRT blueprint. Keep the shared blueprint, Physics warrant library, WPE adapter, and runtime separate.
12. Do not invent a D1/D2 common blueprint; record `SPEC_PENDING`.
13. State explicitly in every PR: **“No academic approval inferred from software validation.”**

## PR template

- **Task / issue subsection:**
- **Files changed:**
- **Behavior implemented:**
- **CLI example and output:**
- **Tests run (verbatim result):**
- **Known blockers / HOLD gates:**
- **Independent review still required:**

## When something is ambiguous

Do **not** guess scientific meaning, examination authenticity, reviewer authority, or cognitive equivalence. Implement the unambiguous mechanical requirements first; add a short `OPEN_QUESTION` note against Issue #1 for the owner to resolve. Prefer small, reversible changes and conservative HOLD reports.

**Green CI means automatic tests passed; it never means student release is authorized.**
