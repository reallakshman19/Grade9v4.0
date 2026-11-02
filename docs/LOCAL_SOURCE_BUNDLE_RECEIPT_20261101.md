# Grade9 v4.0 — Local Source Bundle Receipt and Inspection Reconciliation

**Date:** 1 November 2026  
**Repository Branch:** `feat/core2-template-corrections-and-local-source-receipt`  
**Related Pull Requests:** Draft PR #19 (`oracle/handover-20261101-claude`), stacked on Draft PR #11 (`feat/wep01-real-evidence-readback`)  

---

## 1. Executive Summary

This receipt reconciles the source-inspection findings from the 1 Nov 2026 source-level check against the Grade9v4.0 local working tree (`D:\CodeD\grade9v4`). 

Pursuant to repository rules (**AGENTS.md Rule 9: Provenance and Copyright Protection**) and the Oracle Handover Protocol, proprietary third-party exam question text, official answer keys, textbook scans, and unadmitted learner attempts are **strictly excluded from public Git repositories**. 

To supply the necessary source files to external review and production environments without compromising repository provenance boundaries:
1. The **9 required local artifacts** have been staged and packaged into the private local archive `G9V4_Core2_Core1A_Source.zip`.
2. The **verified code/template defects** identified in the GitHub `templates/` kit have been corrected directly in this branch.

---

## 2. Component Reconciliation Matrix

| Component | Inspection Finding | Reconciled Status | Resolution / Custody Location |
|---|---|---|---|
| **Core2 HTML** | R3 `core2.html` absent from GitHub | **Local Bundle Packaged** | In accordance with copyright/privacy rules, rendered learner HTML containing verbatim question text remains in `workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/rendered/core2.html`. Packaged in `G9V4_Core2_Core1A_Source.zip`. |
| **Renderer** | `build_reader.py` depends on missing `runtime/Shared`, CSS and JS | **Local Bundle Packaged** | The complete native Shared renderer engine, CSS tablet styles, and JS assets are located under `workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/runtime/` and `workspace/native/Grade9v3.5/Shared/`. Packaged in `G9V4_Core2_Core1A_Source.zip`. |
| **Core2 Template** | Exists, but has 59 placeholders and hardcoded NSEP-specific defaults | **CORRECTED in Git** | Updated `templates/core2-exam-card/TEMPLATE-bank.json` and `TEMPLATE-intake.json`. Replaced hardcoded NSEP-specific fields (`multi_correct_mcq`, `OWNER_DECIDED_CELL_APPLY_D2_NOT_ADMITTED`, `PAPER_ON_FILE_NOT_ADMITTED`) with explicit general card placeholders. |
| **QRT Difficulty** | Template defaults to D2 with score 0 — inconsistent with D1/D2 scoring bands | **CORRECTED in Git** | In `templates/core2-exam-card/TEMPLATE-bank.json`, corrected difficulty default from `band: "D2"` to `band: "D1"` when component scores sum to `score: 0` (D1 band is 0–2 points; D2 is 3–5 points). |
| **Browser Testing** | Fixed at 10 cards, NSEP question ID and absolute local paths | **CORRECTED in Git** | Updated `templates/reader-build-kit/browser_check.js` and `run_browser_check.js`. Replaced hardcoded `D:/CodeD/...` paths with `process.env.READER_ROOT` / `READER_SHOTS`. Parameterized card count via `EXPECTED_CARD_COUNT`. Guarded SVG regression checks against missing local baseline assets. |
| **Core1A** | Contracts and source-preparation checker exist; no complete lesson-production pipeline established | **Documented & Packaged** | All 10 preparation dossiers (`WPE-N01` through `WPE-N10`) and source-to-Core1A R2 skills are packaged in `G9V4_Core2_Core1A_Source.zip`. Per Owner decision, lesson construction is gated on Core2 question admission. |
| **Question Inventory** | Registry and exam extraction are not in GitHub | **Local Bundle Packaged** | The 62-question extract (`examside-wpe-extract.json`) and candidate registry (`registry.json`) are Git-excluded to protect source provenance; both are packaged in `G9V4_Core2_Core1A_Source.zip`. |

---

## 3. Local Bundle Artifact Verification (`G9V4_Core2_Core1A_Source.zip`)

- **File Path:** `D:\CodeD\grade9v4\G9V4_Core2_Core1A_Source.zip`
- **File Size:** 14,277,139 bytes (13.61 MiB)
- **SHA-256 Checksum:** `0EDDF529E2C46ABAAA30225E9D3D09D2C451A5EF6D1462DCD3C1F861DC17D200`
- **Total Packaged Entries:** 505 entries
- **Missing Items:** 0 of 9

### Packaged Items Manifest

1. `workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101`  
   *R3 reader: rendered `core2.html`, patched `render_core.py`, tablet CSS/JS runtime, assets, native records, and browser checks.*
2. `workspace/legacy/g9v3.5/qrt/sources/examside-wpe-extract.json`  
   *62-question examination extraction ledger.*
3. `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data`  
   *Candidate registry (`registry.json`) and raw intake.*
4. `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Academic_Review_R1_20261031`  
   *Sealed blind review R1, official keys, and reconciliation reports.*
5. `workspace/output/WPE_Core2_R19_20261101`  
   *Academic review R19 covering candidate questions (M39, M44, M60, M101, NSEP Q57).*
6. `workspace/subjects/physics/blueprints`  
   *Physics QRT blueprints, 5-factor scoring rubric, and resolved sub-tile rules.*
7. `workspace/subjects/physics/adapters`  
   *Work, Power and Energy (WPE) topic adapter draft.*
8. `workspace/native/Grade9v3.5/Physics/library/phy-work-energy-power.v1.json`  
   *Canonical Physics WPE concept library and prerequisites.*
9. `workspace/skills/source-to-core1a-r2/examples/wpe-source-program`  
   *Ten Core1A preparation dossiers (`WPE-N01`..`WPE-N10`), figures, and spine ontology.*

---

## 4. Mechanical Verification

- **Python Version:** 3.14.0 (with `jsonschema` 4.23.0)
- **Test Command:** `python -m pytest -q -p no:cacheprovider`
- **Test Results:** `285 passed, 2 failed, 1 warning in 2.79s`
  - The 2 failures (`test_safety.py::test_symlink_cannot_escape` and `test_subject_workspaces.py::test_symlink_escape_on_subject_contract_is_fail`) are the documented Windows OS symlink-privilege (WinError 1314) limitations, identical to the repository baseline.

---

No academic approval inferred from software validation.
