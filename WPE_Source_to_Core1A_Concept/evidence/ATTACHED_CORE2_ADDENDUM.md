# WPE Core2 — R2 Read-Only Audit: Technical Concept Addendum

**Status:** Proposed changes to `WPE_CORE2_TECHNICAL_CONCEPT_NOTE.md`; not Owner approval, independent admission, or authorization to implement/release.  
**Source inspected:** `WPE_CORE2_R2_READONLY_AUDIT(1).zip` (SHA-256 `16dd1d5aadc9c2cdf0a0c4e120c1249092136829dc9ac2813c127236a63d20c0`).  
**Integrity performed here:** ZIP CRC/`testzip` and SHA-256+byte-size verification of all ten `MANIFEST.json` members: PASS. Audit checker output is a *recorded* result (7 PASS/8 HOLD); its original four-input run was **not** reproduced here. Source `core2.py` and golden `bank.json`/`manifest.json` were spot-checked against the supplied original archives. No source inputs were edited.

## A. Decision: retain the concept's architecture; add an enforceable promotion bridge

The concept correctly distinguishes source review from the Core2 learner product, but the audit demonstrates that this distinction must be **implemented as a stateful, fail-closed promotion service**, not just described.

```text
 ORIGINAL EXAM PAPER / OPTIONS / ORIGINAL FIGURES / KEY VERSIONS
           |               separate question vs answer custodians
           v
  [SOURCE AUTHORITY + SL1 IDENTITY] -- failure --> HOLD / QUARANTINE
           |
           v
  [INDEPENDENT FIRST SOLVE + SL2] -- D1/D2 --> SUPPORT ONLY
           |            compare with exposed proposals only later
           v
  [QRT ADJUDICATION + APPROVAL RECORD]
           |       primary operation, D3/D4, distinct identity
           v
  [BLUEPRINT + APPROVED WPE TOPIC ADAPTER RESOLVER]
           |       validate topic/capability/14 navigation-cell refs
           v
  [HASH-BOUND ADMISSION / PROMOTION GATE] -- failure --> HOLD/VACANT
           |       consumes exact review and source digests
           v
  [GOLDEN-COMPATIBLE MANIFEST + BANK + RECORDS]
           |
           v
  [GOVERNED RENDERER: ATTEMPT > H1 > H2 > H3 > SOLUTION]
           |
           v
  [BEHAVIORAL/ACCESSIBILITY/PRINT + ACADEMIC + OWNER GATES]
           v
     PRIVATE RELEASE CANDIDATE (NOT automatic publication)
```

### Promotion invariant

An output question is selectable in `manifest.selection.core2` **only when**: original exam identity is unique and authenticated; exact text/options/required question assets are present; independent answer/key reconciliation and SL1/SL2/QRT admission are current; primary operation and D3/D4 are confirmed; its blueprint/adapter cell is valid; and every referenced digest matches the versions accepted by the reviewer. Any change in question, figure, options, key version, rubric, blueprint, topic adapter or admission invalidates the corresponding derived review/promotion until rechecked. Preserve old versions and old claims.

The inherited R2 treatment of explanatory figures is different from WPE's normalized question-facing intake: retain native digest/gate semantics as-is; add a *versioned compatibility record* showing each asset's role and stage rather than suppressing integrity HOLDs.

## B. New P0 blockers to add to the concept/implementation plan

| Priority | Audit fact / code locator | Concept amendment | Acceptance evidence |
|---|---|---|---|
| P0-1 | `core2.py:139-145` pins the Blueprint, but `core2.py:329-334` hardcodes 10 scope nodes; `core2.py:336-341` hashes the Blueprint without resolving the `(topic,operation,band)` cell. | Define an actual Blueprint+WPE-topic-adapter semantic resolver with validated foreign keys, 14 navigable operation×band cells and topic prerequisites. | Known-good mapping and deliberately invalid/alternate-adapter mutation tests. |
| P0-2 | Six WPE adapter candidates, five unique hashes; no adapter pin or import. | Require an explicit Owner decision on adapter authority/version, include adapter SHA in `pins.json`, review-subject digest and build provenance. Do not invent a consensus adapter. | Signed selection receipt; stale-result invalidation when adapter changes. |
| P0-3 | `core2.py:474-492` emits static `question_page()` and review catalogue; golden has `manifest.json`, `bank.json`, `records.json`, `response` and `hints`. | Build a *new* derived canonical Core2 package with the governed renderer; keep the administrative catalogue separate. | Schema and link validation; actual attempt/commit/hint/reveal DOM/keyboard/print tests. |
| P0-4 | Only 38/78 identity groups scored pre-comparison; 26 original-figure HOLD, 4 NSEP navigation-only, 1 missing collision datum, 9 unassessed. Nine later assessments are explicitly non-blind. | Treat all these as incomplete or provisional; commission separately designated independent first-pass review; never convert a precomparison diagnostic into an appointed review. | Reviewer appointment and exposure attestation; sealed first scores then adjudication receipts; original question readbacks. |
| P0-5 | 79 local exam source-byte claims match local bytes, but only six records have both local paper/key evidence references and those are not authenticated. | Add a *separate* upstream paper/key custody and versioned answer reconciliation gate. | Distinct source identifiers, authority and question/key item locators, witnesses, hashes and agreement/dispute states. |

## C. Existing R1 selection is unstable — targeted re-adjudication

R1 checkpoint: **14 conditional leads, 7 vacancies, 0 admissions**; different from the older 13/8 freeze. The 79 exam records reconcile to **78 identity groups** because `EX-M4` and `JEE-2026-04-05-S2-Q28` are aliases, not two counting homes.

| Candidate | R1 proposed placement | Audit diagnostic | Required action (no automatic substitution) |
|---|---|---|---|
| EX-M62 | APPLY D3 / 7 | APPLY D2 / 5 | Recheck SL2 chain vs integration anchors; otherwise vacate APPLY. |
| EX-M73 | MODEL D3 / 7 | MODEL D2 / 5 | Recheck model selection vs routine distributed-mass energy integral. |
| EX-M79 | APPLY D3 | SYNTHESIZE D3 | Adjudicate decisive move (coordinated velocity/time/energy) and rest branch. |
| EX-M81 | MODEL D3 | SYNTHESIZE D4 | Adjudicate operation and potential-model prerequisites; only one primary home. |
| EX-M60 | SYNTHESIZE D3 | SYNTHESIZE D3 | Agreement is provisional; still requires authenticated paper/key and appointed review. |
| EX-M56, EX-M61, EX-M69 | REPRESENT D3 | Not assessable without original graphs | Recover exact question/option images; otherwise vacate all affected roles. |
| EX-M101 | JUSTIFY D3 / 7 | Post-exposure JUSTIFY D2 / 5 | Fresh independent score is essential; AIEEE statement item, not cut-spring. |
| WEP07-03 | JUSTIFY D4 / 9 | Original crop not academically assessed; synopsis navigational | Inspect actual question crop and independently key; cannot use synopsis as exact exam stem. |
| JEE-2026-04-04-S1-Q46 | Unselected APPLY D2 | Diagnostic REPRESENT D3 / 6 | A conditional replacement **lead**, not admitted; check vector normalization requirement. |
| JEE-2026-04-04-S1-Q49 | Unselected APPLY D2 | Diagnostic SYNTHESIZE D3 / 7 | Candidate alternative; test vector integration/dot-product as decisive move. |
| JEE-2026-04-06-S1-Q28 | Unselected APPLY D2 | Diagnostic SYNTHESIZE D3 / 6 | Exact work -9.9875J; nearest listed -9.98 is not ordinary 2 d.p. rounding. Key/option HOLD. |
| EX-M4 / JEE friction alias | One item, ambiguous "moved up" | Vertical interpretation needed for 20J | Preserve literal stem; no silent "vertically" insertion. |

Do not fill the three RETRIEVE, three EXPLAIN and one JUSTIFY vacancies with authored variants or D1/D2 questions. The diagnostics also create risk that the *pending* count will shrink during review.

## D. Harden the contract checker: current PASS does not mean quality

The supplied `05_CHECK_CORE2_CONTRACT.py` checks many claims by presence/count/string inspection. It can detect useful omissions but cannot establish semantic correctness or academic admission. Retain its diagnostic output, and add these **behavioral gates**, executed on actual built WPE artifacts:

| New test | Failure injection / asserted result |
|---|---|
| B11 — adapter semantics | Change the adapter to a byte-valid but wrong microtopic; mapping validation must fail. |
| B12 — evidence trust roots | Provide paper/key `*_evidence` objects pointing to wrong item/version; review must HOLD despite the objects' presence. |
| B13 — content/version binding | Alter an option, figure, key version, rubric, adapter or review record without changing ID; admission and render receipt must become stale. |
| B14 — uniqueness | Clone an alias with a new ID and separate home; 21-count check must reject it. |
| B15 — authentic response semantics | A multiple-answer original must not become `single_choice` merely because it has four options. Check grading and attempt state. |
| B16 — real renderer | A source tree containing the string `render_core.py` must not pass. Check actual non-draft render stamps, slots, interactions and offline assets. |
| B17 — staged-answer safety | Before commitment, check DOM, JSON embedded in page, alt-text, SVG, print/PDF, search and keyboard interactions for premature solution/hint exposure. Client-only builds can provide UI gating but **cannot claim cryptographic answer secrecy** without a trusted answer-delivery boundary. |
| B18 — academic vs engineering | Schema/renderer/QA PASS must leave academic and Owner statuses unchanged without matching signed approvals. |

The 7 reported PASS / 8 HOLD are **static check results**, not a complete quality or release verdict. Specifically, source-local hash correspondence is not exam authenticity; presence of `paper_evidence`/`key_evidence` is not proof that those references identify the correct official item; 13 native overlay records do not prove their academic validity.

## E. Proposed derived record fields (additive wrapper, not native SL1/SL2 schema changes)

```json
{
  "promotion_contract_version": "proposed/v2",
  "canonical_exam_identity": "stable-identity-id",
  "aliases": ["source-record-id"],
  "question_digest": "sha256:<exact-stem-options-conditions-figures>",
  "answer_claim_digest": "sha256:<inherited-answer-claim>",
  "official_key_evidence": {
    "status": "HOLD|AUTHENTICATED",
    "paper_version": null,
    "key_version": null,
    "item_locator": null,
    "custody_receipt_ref": null
  },
  "review": {
    "independent_first_pass_ref": null,
    "adjudication_ref": null,
    "native_sl1_digest": null,
    "native_sl2_digest": null,
    "primary_operation": null,
    "sl2_scores": null,
    "band": null,
    "source_role": "HOLD",
    "counting_home": null
  },
  "curriculum": {
    "blueprint_hash": null,
    "topic_adapter_hash": null,
    "resolved_topic": null,
    "resolved_cell": null,
    "capability_refs": []
  },
  "product": {
    "canonical_bank_question_id": null,
    "golden_fixture_test_ref": null,
    "render_receipt_ref": null
  },
  "governance": {
    "academic_acceptance_ref": null,
    "owner_approval_ref": null,
    "promotion_state": "HOLD"
  }
}
```

This is a **conceptual delta**, not a validated or approved canonical schema. Production should reference actual native schemas and supply typed enumerations, `required`, digest formats, provenance/figure roles and foreign-key constraints. Do not overwrite original or inherited records.

## F. Action order, handoff artifacts and decision owners

1. **Owner** selects the authoritative WPE adapter and gives explicit scoped local build/review authorization; appoints an independent academic reviewer separately. Until then prepare documentation only.
2. **Source custodian(s)** acquire exact missing original graphs, page/option scans and official paper/key item/version evidence; publish a read-only evidence ledger and unresolved-ID list, not a false PASS.
3. **Academic reviewer** scores from original question materials, records first-pass solutions and factor warrants before seeing R1 results, and seals review receipts; a separate adjudicator reconciles disagreements including M62/M73/M79/M81/M101.
4. **Engineering implementer** writes the append-only normalized source→golden adapter, binds reviewed curriculum refs, emits manifest/bank/records and produces **one genuine WPE admitted golden fixture** with positive and deliberately failing mutation cases.
5. **QA** runs semantic, strict render, browser, hints, wrong/correct-attempt, accessibility, responsive, offline and print tests; separately records academic and Owner status. Do not scale to 21 until golden passes.
6. **Owner** adjudicates coverage and source gap outcomes, approves the exact evidence- and build-hash-bound deliverable, or records explicit vacancies/HOLDs.

**Missing acceptance evidence remains:** approved topic adapter, official paper/key upstream custody, 21 academic admissions, verified WPE golden output, production renderer QA, and Owner approval. No Core1A/1B work or learner release follows from this audit alone.
