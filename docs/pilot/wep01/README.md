# Physics WPE pilot — original-source academic evidence and WEP-01 authoring comparison

**Evidence status:** The Owner-supplied archives contain actual candidate teaching/assessment records. **Independent Physics, QRT, B1–B7 and learner-runtime qualification: HOLD.**

**Scope:** Grade9 v4.0 is a planned **Physics, Mathematics and Chemistry** learning platform. WPE is the first Physics pilot. The source dossiers in this page are *Physics only* and do not qualify Mathematics or Chemistry.

## Two distinct evidence tracks — DO NOT silently merge

1. **WPE D3.1.1 native construction witness** — Owner archive `WPE_D3_Organized_2026-10-30(1).zip`. Native identity `WPE-D31-1-CONSTRUCTION-REVIEW`. It proposes `RECALL_CLASSIFY_PROPOSED` / `D3_PROPOSED` and cites two Core1A microtopic IDs and three Core1B cycles. This is **not** independently adjudicated to one of the seven canonical QRT operation labels, and it is **not** proven to share the `WEP-01` synthetic v1 construction identity.
2. **WEP-01 authored syllabus-first Core1A/Core1B drafts** — Owner archive `Input sources(4).zip`. Its two WEP-01 candidates both use `CORE1A-WEP01` and `CORE1B-WEP01` role IDs and state `WRITER_DRAFT_FOR_INDEPENDENT_CHECK_NOT_APPROVED`. Their actual full source text is Owner-local and **not committed** to this public repository. No reader or validator may self-select the variant or equate it to D3.1.1.

A third artifact, `WPE_CONSTRUCTION_HANDOFF_SKILL_R1_CANDIDATE.zip`, is a **source-to-Core1A preparation** example with `question_links:[]`; it does not resolve the identity join. The `wpe.zip` browser QA is an **author-only HTML hub** check, not a real learner-runtime/answer-leak assessment.

## Reproduction (local originals; no extraction or publication)

```bash
grade9qa wep-pilot-evidence \
  --d3-archive '/local/WPE_D3_Organized_2026-10-30(1).zip' \
  --handoff-archive '/local/WPE_CONSTRUCTION_HANDOFF_SKILL_R1_CANDIDATE.zip' \
  --hub-archive '/local/wpe.zip' \
  --out out/d311-pilot-evidence.json

grade9qa wep01-pair-audit \
  --inputs-archive '/local/Input sources(4).zip' \
  --out out/wep01-paired-authoring-review.json
```

Both commands verify **exact Owner-supplied archive SHA-256 and selected member byte hashes**, read only fixed small members, and return sanitized metadata: IDs, native status tokens, counts, visibility-reference IDs, source hashes and diagnostics. No exam stems, worked solution excerpts, figures or private learner responses are emitted. Both commands **always return academic/release HOLD** (exit 3 if structurally consistent, 1 on contradiction, 2 for invalid IO).

## WPE D3.1.1 original witness: factual status

| Evidence obligation | Original status | What remains unverified |
|---|---|---|
| B1 cognitive target and demand | HOLD | Classify into seven canonical QRT labels and score demand independently; check direct/prerequisite/authored source role |
| B2 decisive construction | PARTIAL_STRUCTURAL_ONLY | Independent physics model/role and countercase reasoning review |
| B3 Core1A teaching sufficiency | NOT_RUN | Inspect all eight cited teacher steps against every decisive role |
| B4 Core1B fresh reconstruction | NOT_RUN | Validate three cited cycles are independent and not worked-example copies |
| B5 answer protection | LOCAL_PREVIEW_CHECKS_ONLY | Real first-answer durable save, hints, picture/alt text, rubric, exam return leak audits |
| B6 diagnosis/repair/transfer | NOT_RUN | Observed error → wrong node → targeted repair → fresh changed-condition success |
| B7 science/source authority | HOLD | Exact qualified Physics library bytes and step-specific warrants; source/paper/figure/official-key custody |

Original source-register custody is `OWNER_LOCAL_PRIVATE_NOT_FOR_PUBLIC_DEPLOYMENT`. Its historical requested three-authentic-questions-per-subset source archive status is `NOT_RECEIVED` **in that archive's own register**. This does **not** negate the separately uploaded `Input sources(4).zip`; it does mean that the old D3.1.1 source-admission need has not been independently closed by these authored WEP-01 teaching drafts.

The D3.1 Physics authority review remains `LIBRARY_GAP / HOLD`. High-priority expert countercases include work of friction on a body, moving contact and normal work, reference frame for translational K, separate body/system energy accounts, and conditions of conservative interactions. Merely finding matching formulas or the right sign of work is insufficient.

## Two actual WEP-01 draft pairs (not exam question content)

| Attribute | `9e95dde5…` draft | `a886c004…` draft |
|---|---|---|
| Core1A blocks | 11 | 11 |
| Core1B concept cycles | 5 | 6 |
| Distinguishing cycle | — | `CYCLE-ZERO-DISPLACEMENT` |
| Pre-attempt convention refs | `WEP01-C1,C2,C3,C4` | `WEP01-C2,C4,C10` |
| Renderer must enforce hiding | NOT_TESTED | NOT_TESTED |
| Exam questions | NONE (authored examples only) | NONE (authored examples only) |
| Independent authoring approval | HOLD | HOLD |

**Do not decide by cycle count.** The alternative visibility allowances change which conventions appear before the learner's answer. A reviewer must check whether they reveal the decisive route, and independently test actual browser behavior before any Core1B publication.

Provenance (candidate-only; original archives stay outside GitHub):

| Source archive | SHA-256 |
|---|---|
| WPE D3 organized archive | `b664284944de4eb76775a089ecdf795a86cd99d250081625aca700dc90f2356c` |
| Source-to-Core1A handoff | `c14de8a538c2276855a5f911dc9685adbebd159f5c631ff870daba87a05ab681` |
| WPE author HTML hub | `50fb7c1e5cba1a9fba4efea360452ed06cb97efc2f370ab382e6598b13583705` |
| Input sources (4) | `ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565` |

Exact selected member digests are in the local audit report output; those checksums are not publisher signatures or independent Physics certification.

## Actual next reviewer decisions, in order

1. **Owner/subject reviewer:** pick one WEP-01 authored pair *after reading full local original content*, or issue a new revision; do not auto-prefer the six-cycle draft. Preserve both historic bytes and distinguish authoring variants.
2. **Physics reviewer:** verify every material force/body/displacement/angle claim, model assumption and countercase, with canonical original source/library SHA and independently scoped warrants.
3. **QRT reviewer:** independently decide the actual cognitive operation, demand vector, D-band, prerequisite/transfer role, and whether the WEP-01 authoring draft is the **same** proposed construction as D3.1.1 or a separate family.
4. **Core1A/Core1B reviewer:** trace decisive roles in full teaching passages, create/review fresh task response evidence, examine protected first-attempt design and diagnose/transfer fidelity for B1–B7.
5. **Runtime reviewer:** exercise the real learner UI and persistence; first-answer save failure must not reveal the model answer, including image/alt text/rubric/hints and exam return.
6. **Shared native governance:** bind actual independent reviewers to exact current record versions and implement authenticated canonical source admission, not self-declared `APPROVED` JSON.

**Current result: one source-backed reviewer packet and two authored teaching candidates, but zero independently qualified WEP-01 constructions and no learner release.** No Mathematics/Chemistry contents are implied.
