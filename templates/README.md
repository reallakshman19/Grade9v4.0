# Key templates (copied from the Owner-local `workspace/`, 1 Nov 2026)

These are **structure and method only**. Each file was scanned for question text, keys, Drive links and emails before it was copied. The originals stay in `workspace/` (Git-excluded). If a copy here and its original differ, **the original wins**. Copying a file here does not make it approved.

| Folder | Copied from | Use it for |
|---|---|---|
| `core2-exam-card/TEMPLATE-bank.json`, `TEMPLATE-intake.json` | Generated from the NSEP Q57 card in reader R3 (`native/nsep-*.json`); every learner/source value is replaced by `<FILL: …>` | Starting a new exam-question card (handover §6 C). Fill each placeholder; keep the field names. |
| `physics-blueprint/` | `workspace/subjects/physics/blueprints/` | The Physics QRT Blueprint: D3/D4 cells, the 5-factor demand rubric, and the sub-tile blueprint v0.2.1. Physics only; never reuse it for Maths or Chemistry. |
| `shared-web/` | `workspace/native/Grade9v3.5/Shared/web/` | Page blueprints (Core2 source-question, Core1A construction, …) and their schema |
| `shared-roles/` | `workspace/native/Grade9v3.5/Shared/roles/` | What each Core role (Core1A, Core2, Core2A, Core2B) must and must not do |
| `shared-schemas/` | `workspace/native/Grade9v3.5/Shared/library/` | `package`, `competitive-exam-bank` and `source-question-custody` schemas: the shapes a card's records must satisfy |
| `method/` | `workspace/native/Grade9v3.5/docs/method/templates/` | Unit, design-note, worklog, self-critique and Owner-notes templates |
| `skills/smart-labelling-1`, `smart-labelling-2` | `workspace/skills/smart-labelling-r2/skills/` | SL1 (identity and custody) and SL2 (decisive demand) skills, with their references and checker scripts. Candidate tools, not globally installed. |
| `skills/source-to-core1a-r2` | `workspace/skills/source-to-core1a-r2/` (examples and tests left out) | The book-route preparation dossier skill |
| `reader-build-kit/` | Reader R3 (`workspace/output/WPE_Core2_Reader_R3_HintsFirst_20261101/`) | `build_reader.py` wrapper; `patch_renderer.py` (hints-first patch, applied to a **renderer copy only**); `browser_check.js` + `run_browser_check.js` (47 headless checks); `RENDERER_CHANGE.md` + `render_core.diff` |

**Deliberately not copied:**
- `subjects/physics/adapters/root-draft/topic-adapter.work-power-energy.json`: it contains exam question text.
- Every native bank, intake or record file holding real questions.
- Golden fixtures, scans, PDFs and review outputs.

The canonical Shared renderer itself (`runtime/Shared/tools/render_core.py`) is not copied either. Use the pinned original in `workspace/native/Grade9v3.5/Shared/`.

No academic approval inferred from software validation.
