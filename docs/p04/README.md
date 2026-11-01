# P0.4 — B1–B7 bidirectional teaching/reconstruction evidence

**Implementation:** evidence validation + non-compensatory qualifications, candidate-only. **Independent academic qualification:** HOLD.

This follows the actual **Teaching-to-Reconstruction Bridge Witness** obligations from the user-supplied `WPE_D3_Organized_2026-10-30(1).zip` QRT concept note. The note specifies a **derived validation witness**, *not* a new common Physics Blueprint schema. Source archive SHA-256: `b664284944de4eb76775a089ecdf795a86cd99d250081625aca700dc90f2356c`.

## Contracts, CLI and syntax

- `schemas/v1/bridge-witness.schema.json` — standalone **candidate v1 evidence envelope**, not an extension/replacement of QRT's academic Blueprint or Shared's canonical records.
- `src/grade9qa/bridge_witness.py` — B1–B7 independent evidence gaps, contradictions and review-receipt scope checks.
- `src/grade9qa/bridge_legacy.py` — sanitized readback of original archived candidate statuses, preserving PARTIAL/HOLD/NOT_RUN without converting to a qualified v1 witness.
- `examples/wpe-b1b7-candidate/witness.json` — **fully synthetic**, not authentic examination evidence, not a qualified lesson.
- `tests/test_bridge_witness.py`, `tests/test_bridge_legacy.py`, `tests/test_qualify_bridge_integration.py` — positive/negative regression controls.

```bash
python -m pip install -e ".[dev]"
grade9qa bridge-witness --witness examples/wpe-b1b7-candidate/witness.json --out out/bridge.json
# expected: mechanical=HOLD, qualification=HOLD, exit 3

grade9qa qualify --bundle examples/wpe-n01-candidate/bundle.json --out out/qualification.json
# optional --witness <matching-construction-id-witness.json>

grade9qa bridge-legacy --witness /local/original/bridge_witness.json --out out/legacy.json
# archived native candidate format remains HOLD, original exam content not echoed
```

**Exit codes:**
- `bridge-witness` / `bridge-legacy`: 1 for structural contradiction, 2 input/IO, 3 HOLD. There is no route to automatic academic PASS.
- `qualify --witness`: 1 for invalid schema/JSON or existing invalid bundle; 2 IO; **4 for a known B1–B7 contradiction** or a witness bound to a different construction; 3 for missing independent approvals or evidence. Aggregate scores cannot override any FAIL.

## Source-derived witness requirements and software boundary

| Gate | Actual source requirement | Implemented mechanical checks | What requires independent review |
|---|---|---|---|
| B1 | Decisive operation, five demand factors, direct/bridge/authored role | Operation, D-band, five-factor numeric band, source-role and QRT receipt references | Authentic task demand and independently reviewed source role |
| B2 | Input, obstacle, decisive move, output, dependencies, conditions and check | Typed signature, nonempty dependency/condition and stable protected role IDs | Whether the reasoning pattern genuinely matches the question |
| B3 | Exact taught spans for every necessary role, worked example, why/boundary/repair | Core1A seven slots, each role's span and demonstration reference, direction and content/example pins | Whether those spans *fully demonstrate* all assessed reasoning |
| B4 | Fresh protected Core1B task with same decisive operation and changed context | Every role observable, distinct task vs teaching hash, direction and freshness-review reference | Genuine conceptual freshness, not merely changed numbers or IDs |
| B5 | Audit hint, picture, alt text, model response, rubric, exam return and first-save state | Six exposure channels, ordered attempt trace, first-save durability and fail-closed save exception | Real browser/runtime enforcement, including alternative paths and assistive text |
| B6 | Misconception → failed node → Core1A repair → changed-condition probe → success | Role-linked diagnosis, erroneous node, repair span and observable transfer criterion; absence of learner answer is INSUFFICIENT_EVIDENCE | Whether diagnosis is valid and transfer actually demonstrates successful reconstruction |
| B7 | Version-pinned qualified Physics warrants per consequential step; source/figure/key custody | Role-to-warrant digest/reference pins; independent Physics and custody references; explicit exam paper/key/solution obligations | Scientific truth, exact external authority, source authenticity and independent approval |

**Direction is non-symmetric:** if Core1A teaches potential→force but Core1B tests force→potential, B3/B4 fail. Matching topic, equation or legacy construction ID is insufficient.

## Underlying archived WPE candidate readback (local; not imported)

- **D3.1**: six distinct candidate `bridge_witness.json` records: B1 HOLD; B2 PARTIAL_STRUCTURAL_ONLY; B5 LOCAL_PREVIEW_CHECKS_ONLY; B7 HOLD. Other obligations NOT_RUN. No academic approval.
- **D3.6**: `B1_B7_TWO_WAY_WITNESSES.json` has four aggregated candidate witnesses. All B5/B7 HOLD; B3/B4 partial or HOLD. Some originally proposed D3 cognitive constructions independently looked closer to D2, or required reverse-stage teaching absent from Core1A. Do **not** average those objections away.
- **D3.5**: force→potential and potential→force require different directional teaching; an original inverse example remained a candidate and was not accepted as compiled, reviewed instruction.

`bridge-legacy` reads these older formats and outputs **only source-native B-status values and candidate IDs**, never exam stems, learner data, screenshots or the original passages. Its statuses are source claims, not attestations.

## Trust and release boundaries

- **A JSON file with `decision:APPROVED` is not a signed/trusted review.** The engine checks reviewer != author, subject digest, exact gate and discipline, but deliberately returns HOLD even when every apparently valid receipt is supplied. Shared's *original trusted authority* must verify identity, digest, policy and actual authorized review events.
- The engine **does not judge Physics correctness or cognitive adequacy with keywords**. Machine completeness cannot replace independently read teaching and learner-task passages.
- Claimed browser-state events and source hashes are only metadata unless verified against the real published learner runtime and pinned files.
- No weighted MCDA, page count, synthetic task or native checker PASS is sufficient for learner release.
- Independent Shared/QRT/Physics governance, complete accepted WEP-01 pilot, and actual browser tests remain required.
- The platform is public. Do not copy the full original D3 archives, third-party exam question text or restricted source material into GitHub without authorization.

## Required next steps

- [ ] Obtain independently reviewed source-to-Core1A teaching spans and Core1B fresh task, including relevant counterexamples.
- [ ] Run native (not synthetic) browser tests: desktop/mobile, hints, pictures, alt text, exam return, save exceptions, persistent first attempt.
- [ ] Use Trusted Shared to independently verify scoped reviewer receipts; connect only verified decisions as a future **separate** release-gate integration.
- [ ] Verify canonical Physics library byte pins and real exam source/figure/key custody.
- [ ] Run genuine adversarial cognitive mutation tests (same ID with different operation, inverse translation without teaching).
- [ ] Qualify one WEP-01 construction before counting or scaling lessons.

**P0.4 machine evidence engine is implemented. P0.4 independent academic acceptance remains HOLD.**
