# Renderer change: a candidate change to Shared, not installed

**Owner decisions:**
1. "Yes, hints first."
2. Then "Allow before attempt": hints can be used at any time, one rung per click. The full answer and working opens only after an attempt AND a press of its own button.

**Where the change lives.** The reveal logic is the runtime JavaScript that `Shared/tools/render_core.py` embeds as its `JS` string, together with the HTML that file emits. The `js/` folder only holds the header and display controls. So the change could only be made in the renderer.

**What was edited.** Only R3's private copy, `runtime/Shared/tools/render_core.py`, was edited.
- For this revision the copy was first restored to the R1/R2 bytes and then re-patched by `patch_renderer.py`. Each of its 6 replacements is asserted to match exactly once.
- File hash before: `0ec1acc7…cceb06`.
- File hash after: `cc236ecf…094f0`.
- The full diff is in `render_core.diff`.
- No canonical Shared file was changed.

## What changed (current version)
1. Core2 hint panel: only the label changed, to "Need a hint? · one at a time". It is **not** gated, so hints can be used before an attempt, as in R1 and R2. The ladder still opens one rung per click.
2. Core2 TRAP: the separate "Common wrong route · after your attempt" reveal is removed.
3. Core2 SOLUTION: one reveal, **"Show full answer and working"**. It holds the steps, the key, the common wrong route, the check and the rationale. It stays behind the existing attempt gate, so it is locked before an attempt and can only be opened by its own button after one. Nothing opens it automatically.
4. Runtime JavaScript:
   - `saveCore2State` also stores `hints` (whether the hint panel is open) and `full` (whether the full answer is open).
   - `restoreCore2State` reopens the hint panel whenever it was open, and the full answer only when there is a saved attempt.
   - A `toggle` listener on both saves every change.
   - The rung counts and per-rung reveal states were already saved and are unchanged.

## Dropped from the first R3 version
The `gated` flag that the first version added to `secondary_disclosure` has been removed.

## Side effects to review
- Opening the common wrong route was recorded as the "WRONG_ROUTE" assistance marker. That marker is no longer recorded, because the old listener now finds nothing. Opening the full answer is not recorded as assistance either.
- **Shared tests: NOT_RUN.** Only the R3 author browser checks were run.

No academic approval inferred from software validation.
