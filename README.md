# Grade9 v4.0 — Physics, Mathematics and Chemistry Learning Platform

> **Product scope:** The application is planned for **Physics, Mathematics and Chemistry**. WPE is the first **Physics pilot topic**, not the application or universal curriculum. Current Grade9QA contracts and sample assets are pilot-scoped; a **v2 candidate intake contract** exists in draft PR #7, while native subject adapters, canonical migration and Mathematics/Chemistry blueprints are **not yet implemented**. See [product scope and migration plan](docs/product-scope.md).

The initial candidate validator and Smart Skills read-only adapter are documented in [draft PR #2](https://github.com/reallakshman19/Grade9v4.0/pull/2), following [master specification #1](https://github.com/reallakshman19/Grade9v4.0/issues/1).

## P0 Core2 three private Owner review batches (draft PR #17)

[Draft PR #17](https://github.com/reallakshman19/Grade9v4.0/pull/17) converts the six previous Core2 representation warnings into three actionable, **independently reviewed** handoffs: (1) three reasoned potential waivers; (2) two original, private, answer-free SVG authoring candidates; (3) the ILL-05 original-source missing initial-speed Physics HOLD. It adds fail-closed identity, SVG, native provenance and anti-approval tests; **no real waiver, figure binding, exam admission or new learner HTML is made**. See [R17 source-backed three-batch work order](docs/core2-three-batches/README.md).

## P0 Core2 representation applicability: six original source records (draft PR #16)

The original Shared Core2 Blueprint 1.11.0 declares `REPRESENTATION` as **EXPECTED**, allowing a specific written **author waiver** where diagrams would be decorative or reveal an answer. [Draft PR #16](https://github.com/reallakshman19/Grade9v4.0/pull/16) reviews six original ten-gap receipt records: **3 waiver proposals, 2 neutral-visual authoring routes, 1 missing-initial-condition Physics/source HOLD**. Two existing solution-only FBD/chain figures remain protected post-attempt. **No waivers were actually applied, no new diagrams created, all original 10 render gaps unchanged.** [Owner source/Blueprint-based plan](docs/core2-representation/README.md).

## P0 Core2 native SVG warning repair candidate (draft PR #15)

The original `Input sources(4).zip` does contain editable candidate SVG files for the four flagged WPE figures. [Draft PR #15](https://github.com/reallakshman19/Grade9v4.0/pull/15) proposes a byte-pinned fix to the original Shared SVG label checker—decoding numeric entities, respecting parent transforms and preserving real clipping and tablet text-size warnings—without changing the original figure assets or native receipt. The **six separately missing source `REPRESENTATION` components remain HOLD**. See [actual source/Chromium evidence](docs/core2-native-svg/README.md).

## P0 Core2 SVG evidence: retain existing figures, investigate renderer false positives

[Draft PR #14](https://github.com/reallakshman19/Grade9v4.0/pull/14) measures **transformed SVG text bounds** in Chromium against the actual original native nine-card `core2(3).html` and its ten-gap render receipt. The four `AUTHOR_FIGURE_TEXT` cases all had visible-browser text inside the viewBox at 1280×850, suggesting conservative false positives in the original character-width heuristic. **No original Shared warning was waived or source SVG changed.** Six missing `REPRESENTATION` components still need real native source and reviewer decisions. See [exact geometry and authoring backlog](docs/core2-geometry/README.md).

## P0 Core2 native runtime repair (draft PR #13)

[Draft PR #13](https://github.com/reallakshman19/Grade9v4.0/pull/13) provides a **source-independent, Owner-local patch** for the existing original Shared `render_core/2` **Core2** runtime: verify first-response storage and readback **before** solution reveal, preserve first committed answer, and remove the author debug reveal function from Core2 pages. Private tests against the existing **nine-card** native HTML passed five Chromium interactions; 11 new synthetic regression tests passed CI. No original Shared renderer, full HTML, question text, figures, answers or Owner files are committed to GitHub.

The **ten original authoring/diagram receipt gaps remain open**, as do the trusted native rebuild, server-protected answers, Owner-selected WPE adapter, original exam authentication, independent QRT/Physics/Core2 admission, and learner release. See [native Core2 runtime evidence and limitations](docs/core2-runtime/README.md).

## P0 Core2: no duplicate HTML, source identity and Physics QRT binding

[Draft PR #12](https://github.com/reallakshman19/Grade9v4.0/pull/12) adds `core2-inventory-audit` and `core2-cell-audit`, using the original **four review lots (63 identified source IDs + 16 reconciliation positions)**, **21-place selection (14 conditional / 7 vacant)** and **nine existing native Core2 rendered cards (8 textbook / 1 synthetic)**, which must **not** be conflated. The original Physics Blueprint supplies 14 D3/D4 cells but the current general WPE adapter candidate supplies only D3.1 and is unselected; the later subtiles refer to a different Blueprint version. Everything remains an academic HOLD; the native renderer is reused, not replaced.

See [Core2 P0 source-based plan](docs/core2-p0/README.md).

## P1 pilot: original WPE evidence and authored WEP-01 drafts (draft PR #11)

The Owner-provided source archives include a **noncanonical D3.1.1 B1–B7 witness** and **two actual WEP-01 Core1A/Core1B authored pairs**. They must not be silently equated. The `wep-pilot-evidence` and `wep01-pair-audit` commands read fixed ZIP members locally, preserve original SHA-256 byte identities and produce **metadata-only academic HOLD** reports; they never publish original exam/teaching text, approve academic correctness or test the actual learner runtime.

See [WEP-01 reviewer packet](docs/pilot/wep01/README.md) and [draft PR #11](https://github.com/reallakshman19/Grade9v4.0/pull/11).

## P0.5c — Real Shared subject-workspace preflight (draft PR #10)

`grade9qa subject-workspace-audit` examines a **real provided repository root**, looks for each explicitly bound `<Subject>/adapter/CoreContracts.json`, checks the native six-Core catalogue and claimed validator limitations, and compares subject-local gate/library evidence to Shared's native discovery result. It never executes or installs a subject adapter or grants academic approval.

```bash
# Native Shared checker runs separately in a trusted full subject repository:
python -B Shared/tools/check_subjects.py > /local/native-subjects.json

grade9qa subject-workspace-audit \
  --manifest examples/three-subjects-candidate/manifest.json \
  --root /path/to/full-subject-repository \
  --bindings /local/subject-directory-map.json \
  --native-report /local/native-subjects.json \
  --out out/native-workspaces.json
```

The subject-directory bindings must name **actual owner-authorized directories**. The supplied `Shared.zip` has no such subjects. A synthetic three-subject local native run reported `passed:true` with all three `CONTRACT_ONLY` and zero gate/library records; **this is NOT three-subject readiness**. `subject-workspace-audit` retains HOLD even when native discovery passes. See [preflight guide](docs/native-subject-workspaces/README.md) and [draft PR #10](https://github.com/reallakshman19/Grade9v4.0/pull/10).

## P0.5b — WPE v1 migration preview and native Shared subject-dispatch readback (PR #9)

`migrate-v1-preview` creates a **reversible, read-only reference map** from the historic Physics/WPE WEP-01 pilot to the versioned three-subject v2 candidate intake. It records original bundle/collection/source byte hashes, preserves original IDs and statuses, and refuses unverifiable source assets or silent transfer of an old APPROVED status.

```bash
grade9qa migrate-v1-preview \
  --bundle examples/wpe-n01-candidate/bundle.json \
  --manifest examples/three-subjects-candidate/manifest.json \
  --out out/v1-migration-report.json \
  --candidate-out out/v2-candidate-preview.json

# Only with actual native Shared/tools/check_subjects.py output
# and an explicit, owner-reviewed subject-directory binding map:
grade9qa shared-dispatch-audit \
  --manifest out/v2-candidate-preview.json \
  --native-report /local/shared-subject-check.json \
  --bindings /local/subject-directory-bindings.json \
  --out out/shared-subject-dispatch.json
```

The **original standalone Shared.zip** yields zero native subject workspaces: no subject is installed or academically approved in that snapshot. The migration intentionally leaves `lessons`, `assessments` and `approvals` in their original v1 custody and flags legacy Physics Blueprint/adapter aliases as review-required, not automatically equivalent.

`schemas/v1` and native Shared contracts are unchanged. A structurally usable candidate returns exit **3/HOLD**; a failed check returns **1/FAIL**; malformed/unreadable inputs return **2**. See [P0.5b guide](docs/v2-migration/README.md), [PR #9](https://github.com/reallakshman19/Grade9v4.0/pull/9), and [Issue #8](https://github.com/reallakshman19/Grade9v4.0/issues/8).

## Three-subject v2 candidate intake (stacked PR #7)

The `subjects-audit` command validates a **subject-neutral candidate intake** for Physics, Mathematics and Chemistry, with type-aware scoped references and exact Blueprint/adapter identity checks. It deliberately does **not** replace the Shared canonical library, create native subject adapters, or approve Mathematics/Chemistry syllabuses.

```bash
grade9qa subjects-audit \
  --manifest examples/three-subjects-candidate/manifest.json \
  --out out/subjects-audit.json
```

The example has the WPE/WEP-01 **Physics pilot** and explicitly PLANNED Mathematics and Chemistry subject entries with no fabricated Blueprint or lesson. Exit **3/HOLD** means candidate structure is mechanically consistent but subject qualifications are absent; exit **1** means a contradiction. The legacy v1 WPE commands and fixtures still work. See [v2 contracts and migration notes](docs/v2/README.md).

## Implemented in P0.0–P0.1 and early Smart Skills adaptation

- Python 3.11+ installable package and `grade9qa` command.
- Eight versioned evidence JSON Schemas.
- Local bundle loading, schema errors, type-aware references, duplicate IDs and prerequisite cycles.
- Numeric D1–D4 rubric-band consistency checks (not academic validity).
- Sample WEP-01 **synthetic candidate**, pytest suite, and Python 3.11/3.12 CI.
- The new `smart-audit` reads native Smart Labelling R2 reports without asserting qualification; native skills are **not** installed by this repository.
- B1–B7 candidate evidence checks are implemented in PR #6, but **independent academic approval and learner release remain HOLD** pending native reviewer authority and real learner evidence.

## Run locally

```bash
python -m pip install -e ".[dev]"
grade9qa validate --bundle examples/wpe-n01-candidate/bundle.json --out out/validation.json
grade9qa bridge --bundle examples/wpe-n01-candidate/bundle.json --out out/bridge.json
grade9qa qualify --bundle examples/wpe-n01-candidate/bundle.json --out out/qualification.json
grade9qa report --bundle examples/wpe-n01-candidate/bundle.json --json out/report.json --md out/report.md
grade9qa smart-audit --report path/to/native-r2-report.json --out out/smart-audit.json
python -m pytest -q
```

See [readme.txt](readme.txt) for **“1. Correct workflow placement”** and [Smart Skills integration](docs/smart-skills-integration.md) for the R2 candidate adoption rules.

The sample has mechanically valid candidate records. `qualify` intentionally returns exit code **3 (HOLD)**. This is not a software defect. No source scan, official paper, answer key or academically approved lesson is provided.

## P0.4 B1–B7 teaching-to-reconstruction witness (stacked PR #6)

Grade9QA now includes a **candidate-only, non-compensatory B1–B7 evidence checker**. This supplements rather than replaces native Shared/QRT/Physics governance.

```bash
grade9qa bridge-witness --witness examples/wpe-b1b7-candidate/witness.json --out out/bridge.json
grade9qa bridge-legacy --witness /local/original/bridge_witness.json --out out/archived-status.json
grade9qa qualify --bundle /local/valid-bundle.json --witness /local/matching-witness.json --out out/qualify.json
```

Known contradictions in operation, direction, reused worked task, protected-answer exposure, false first-save, scientific warrants or review record cause FAIL. Missing independently qualified evidence remains HOLD, even when structural witness fields are complete. **No academic PASS/release can be manufactured from an untrusted JSON approval receipt.** Details and original-source limitations: [P0.4 documentation](docs/p04/README.md) and [PR #6](https://github.com/reallakshman19/Grade9v4.0/pull/6).

## P0.3 native QRT/WPE binding (stacked PR #5)

`grade9qa qrt-bind` checks candidate **SL1 → SL2 → native R2 sidecar → QRT Physics Blueprint v0.2.0 → WPE topic adapter** consistency, with an optional source-to-Core1A preparation dossier.

```bash
grade9qa qrt-bind --sl1 /local/sl1.json --sl2 /local/sl2.json \
  --contract /local/native-sidecar.json --blueprint /local/physics-blueprint.D3-D4.json \
  --adapter /local/topic-adapter.work-power-energy.json \
  --handoff /local/source-to-core1a-handoff.json --out out/qrt-binding.json
```

It checks IDs, native legacy SL1/SL2 digest continuity, proposed operation, five-factor demand scores, exact Blueprint/adapter cells, preparation-only handoff status and optional native checker reports. **It never approves QRT cognitive demand, a scientific warrant, exam authenticity, teaching equivalence or release.** The original QRT WPE adapters contain examination text and are intentionally kept out of this public repository. See [P0.3 documentation](docs/p03/README.md) and [PR #5](https://github.com/reallakshman19/Grade9v4.0/pull/5).

## P0.2b complete inventory and native authority report adapter (stacked PR #4)

The 292-file `Shared.zip` is **external** and has not been republished in this public repo. The read-only tools create a deterministic per-file SHA-256 inventory and summarize the original Shared auditors' **native reports**. They **never grant academic approval**.

```bash
grade9qa shared-manifest --archive /path/to/Shared.zip --shared-root /path/to/Shared --out out/shared-full-manifest.json

# The following inputs must be outputs of the original Shared auditors, not reports invented by Grade9QA:
grade9qa shared-authorities --core core-authority.json --review review-audit.json --release release-audit.json --out out/native-authorities.json
```

Exit 3 means the evidence is mechanically usable but platform/academic qualification remains **HOLD**; exit 1 means contradiction/invalid evidence; exit 2 means unreadable inputs. A native audit with **zero receipts** cannot establish a reviewed record or authorized learner release. See [P0.2b instructions](docs/p02b/README.md) and [draft PR #4](https://github.com/reallakshman19/Grade9v4.0/pull/4). 

## Shared platform audit (stacked PR #3)

The existing Shared platform is **not yet copied into this public repository**. Its 292-file owner-supplied archive is summarized by 16 selected immutable source fingerprints in `docs/shared-baseline-pins.json`.

```bash
grade9qa shared-audit --shared-root /path/to/extracted/Shared --archive /path/to/Shared.zip --out out/shared-audit.json
```

This reads the external archive/snapshot, checks selected source fingerprints, six-Core authority invariants, cognitive operation mapping and Grade 9 Physics scope. It never executes upstream code or grants approval. Exit **3** means mechanical audit completed but independent integration/academic review remains **HOLD**.

See [Shared compatibility audit](docs/shared-compatibility-audit.md) and the [stacked PR #3](https://github.com/reallakshman19/Grade9v4.0/pull/3). The parent PR #2 must merge first.

## Layout

- `schemas/v1/`: source, warrant, construction, lesson, assessment, approval, bundle, report.
- `src/grade9qa/`: CLI and partial validators; academic gates unimplemented and blocked.
- `examples/wpe-n01-candidate/`: entirely synthetic test evidence.
- `tests/`: automatic regressions.
- `docs/`: architecture, schema rules, import policy and independent reviewer checklist.

## Non-negotiable boundaries

Hash verification is not Physics approval; a shared formula is not teaching-to-reconstruction equivalence; D3/D4 demand is not a school grade; a green build is not permission for student release. Do not invent review receipts, exam authenticity or D1/D2 standards. Source archives remain outside this public repo pending proper permission and custody.

See [AGENTS.md](AGENTS.md) for coding-agent instructions and [implementation status](docs/implementation-status.md) for open phases.
