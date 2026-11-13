# Start here — Grade9 v4 local workspace

Use **D:\CodeD\grade9v4** as the working directory. Read this page before editing, importing, running a build or briefing another agent. This is the Owner's local working checkout; the public branch remains a candidate engineering foundation.

```powershell
Set-Location 'D:\CodeD\grade9v4'
git branch --show-current
git rev-parse HEAD
```

Expected branch `feat/wep01-real-evidence-readback`; migration baseline commit `38485dc8ef7f8af5d86031beab6ab565b2c61f25`. Later branch changes require a fresh comparison. Local migration changes are uncommitted. No remote update is authorized by this file.

**Open the [linked local entry page](index.html).** Also read [repository instructions](AGENTS.md), [master Issue #1](https://github.com/reallakshman19/Grade9v4.0/issues/1), [product scope](docs/product-scope.md), [implementation status](docs/implementation-status.md), [migration validation](workspace/migration/MIGRATION_REPORT.md) and [current checkpoint](CURRENT_CHECKPOINT.md).

## Required conceptual reading — every new agent

A dispatcher arranging a sealed blind academic review must instead provide the [source-only reviewer packet route](docs/agent-entry/07-independent-review.md) before exposing this page’s current outcomes. Do not claim a blind review after reading prior exact-task classifications.

[Open the agent onboarding HTML](docs/agent-entry/index.html) and [follow the ordered reading map](docs/agent-entry/00-required-reading.md). The [Source → Core1A concept report](docs/agent-entry/concept-report-v4.html) and [revised QRT methodology](workspace/legacy/g9v3.5/chatgpt/output/QRT_Methodology_Concept_Note_REVISED_WITH_APPENDIX.md) explain WHY the pipeline exists. Read the [current companion](docs/agent-entry/CURRENT_CONCEPT_COMPANION.md) alongside the historical report: one-dossier and14-lead statements are dated evidence. Then inspect the [worked R2 dossier](workspace/skills/source-to-core1a-r2/examples/wpe-source-program/handoffs/WPE-N01.json) and [fixtures/controls](docs/agent-entry/fixtures.html) before using the assigned contracts.

## Aim and actual scope

Grade9 v4 targets Physics, Mathematics and Chemistry. Shared/native canonical records and six Core role boundaries govern the platform. WPE is only the Physics pilot. Grade9QA reconciles evidence and B1–B7; it does not replace Shared, native SL1/SL2, subject QRT judgment, scientific reviewers or release authority.

The local native snapshot contains existing subject directories for reference. Their presence is not V4 subject selection, full curriculum implementation or approval. Mathematics/Chemistry first-topic decisions and their independent Blueprints remain pending. Never generalize the Physics Blueprint, WEP IDs or `qrt-bind` to those subjects.

## Process path and agent entry points

| Stage | Start with | Actual output / decision |
|---|---|---|
| Source intake | [01 source agent](docs/agent-entry/01-source-intake.md) | Stable source identity, exact text/figure/key/locator custody; separate examination, textbook, reference, authored and synthetic roles |
| Skills | [02 Smart Skills agent](docs/agent-entry/02-skills.md) | Native SL1 identity and SL2 cognitive candidate records/checker reports; no automatic approval |
| Blueprint + topic adapter | [03 subject/QRT agent](docs/agent-entry/03-blueprint-adapters.md) | Pinned subject rules, compatible topic binding, independent operation/demand/source-role decision |
| Output construction | [04 output agent](docs/agent-entry/04-output.md) | Native Core2; qualified source/warrant/binder preparation; Core1A/B only under the actual Owner authoring scope |
| Verification and HTML | [05 QA/publication agent](docs/agent-entry/05-qa-publication.md) | Exact build evidence, independent reviews, local review HTML; publication separately gated |
| Oracle continuity | [06 Oracle/reviewer entry](docs/agent-entry/06-oracle-review.md) | Current aim, authority, unresolved evidence and next bounded task; disclose author exposure |

Read the machine [active path map](docs/agent-entry/CURRENT_PATHS.json) and [workflow dependencies](docs/agent-entry/CURRENT_WORKFLOW.json). The migration versions are frozen baseline evidence; use the active maps for current work. The process caption source→skills→Blueprint/adapters→output→publish HTML is a navigation aid: Blueprint/adapter authority is already an input to classification, and book-to-Core1A preparation may proceed in parallel. No universal authority order is inferred from execution order.

## Local directories and custody

```text
src/grade9qa/       checked-out V4 evidence/reconciliation engine
schemas/           historical v1 WPE + candidate subject-neutral v2
docs/              V4 contracts and new agent entry guides
workspace/         OWNER-LOCAL, GIT-EXCLUDED; never git add -f
  legacy/g9v3.5/   original-layout snapshot of the prior local workspace
  native/Grade9v3.5/  pinned Shared, subject references, templates and renderer
  imports/Downloads/  received Owner and engineering handoffs
  skills/          native R2 candidate tools, not global installation
  subjects/physics/blueprints/  Physics-only draft authority references
  subjects/physics/adapters/   root draft; operation variants retained separately
  sources/         future source intake; existing intake resolved by PATH_MAP.json
  output/          future builds/reports; previous outputs remain in legacy snapshot
  publish/html/    LOCAL review entry, not a public deployment
  migration/      manifests, copy/pin/sequence verification and resource receipt
```

Never put protected textbook/exam scans, question text, private assessments or learner data into Git or a public HTML release by assuming a local copy grants publication rights. Original native sources/archives are preserved; metadata and checksums do not supply independent approval. Per-file identities and explicit exclusions are recorded. Historical Windows shortcuts/absolute paths are archival references; new entry points use local relative paths.

## Current WPE frontier

- Examination target21: four exact nominations independently reviewed D2, ten nominations unreviewed, seven original vacancies, eleven slots without currently supported D3/D4 candidates, zero admissions.
- WEP07-03 paper and key agree; prior source-conflict claim withdrawn. Read the corrected academic report, not superseded audit conclusions.
- Current native reader: eight textbook questions plus one synthetic control. Real examination conversion and distinct technical QA remain open. The corrected reader retains nine inherited representation findings plus eight intentional audit-Conditions omissions; the historical22 shell-link occurrences were not re-counted in this documentation pass. See the [current reader receipt](workspace/output/WPE_Core2_Reader_Fix_R1_20261031/review/DELIVERY_RECEIPT.json).
- This chat's Core1A work: ten-node preparation, zero new qualified lessons. Separately, two legacy WEP-01 authored draft pairs may be available as unselected candidates; do not merge their identity with D3.1.1 or treat copying as approval.
- Core1B: no new lesson constructed by this chat. Preserve actual Owner-scoped Core2→approval→Core1A→approval→Core1B authoring gates. Canonical preparation is not universally blocked by Core2 custody.
- D3.1 remains PAUSED. No lesson construction, admission, installation into the user's global skill directory, push or release was authorized by migration.

## Reproduce mechanical checks

The default Python has jsonschema; local `workspace/test-tools` supplies the repository-specified pytest range. It is excluded from Git and can be recreated from pyproject.toml. It does not change the global Python environment.

```powershell
$env:PYTHONPATH = "$PWD\src;$PWD\workspace\test-tools"
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest -q -p no:cacheprovider
python -m grade9qa --help
python tools/verify_local_workspace.py
```

These are instructions, not standing cost or execution grants. Obtain the actual session role/task authorization and a fresh resource bound when needed. Reuse the selected role across compaction; do not rerun role selection in an existing chat. A new agent/session follows its Owner instructions and reads the exact named task before writing.

**Mechanical checks ≠ scientific qualification ≠ learner-runtime acceptance ≠ release. No academic approval inferred from software validation.**


## Migration verification and current limitations

All154registered inputs and12recorded upstream pins have actual local matches; all16,728copied files and36SmartR2members passed full source/destination readback. The Shared archive matches292/292files. See [final verification](workspace/migration/FINAL_VERIFICATION.json).

V4 pytest: **285passed,2failed** because Windows denied symlink creation; those checks remain unresolved. The received branch also contains one **59-character Shared digest**. The original baseline is preserved; a separate [correction proposal](workspace/migration/SHARED_PIN_CORRECTION_PROPOSAL.json) and candidate readback demonstrate the actual source match without rewriting canonical authority. The corrected reader has one targeted V4 build with privately retained runtime assets; general old-build relocation remains NOT_RUN. See [full migration report](workspace/migration/MIGRATION_REPORT.md).
