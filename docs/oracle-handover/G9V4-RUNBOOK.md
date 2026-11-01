# Grade9 v4 buddy runner: runbook (DRAFT, 1 Nov 2026, not yet agreed by the Owner)

Modelled on the TopoFix runner (Owner idea, 31 Oct 20:43). A cheap Sonnet subagent runs the local checks on each return from the ChatGPT agent A1-G9v4 (chat 6ae5c904, built-in browser tab "tab-1"). A1 cannot run anything on the Owner's machine or see V4's private files; the runner does that.

**Order at each return:** runner (fixed result) → independent physics/source reviewer, only when the return makes a physics or answer claim → Oracle decides → Owner says yes before anything reaches the learner or main.

## What a return is
A1 reply with: a draft PR on `reallakshman19/Grade9v4.0` (PUBLIC repo) and/or a private ZIP the Owner downloads into `D:/CodeD/grade9v4/chatgpt/`.

## Rules
- Read-only. No commits, pushes, PR comments, merges, uploads or messages to A1.
- Use a git worktree under the scratchpad: `git -C D:/CodeD/grade9v4 fetch -q origin pull/<N>/head:rb-<N>` then `git worktree add "$S/rb-<N>" rb-<N>`. Never switch the Owner's checkout (branch feat/wep01-real-evidence-readback, uncommitted local work). Remove the worktree when done.
- ZIPs: list members and hashes; extract only into a new empty scratch folder; never run code from them.
- Never print question text, figures, keys or learner data in the result. Report counts and file names only.
- Report NOT_RUN for anything not run.

## Checks
1. **Identity:** PR head SHA and base; ZIP size, SHA-256, member count, CRC.
2. **Tests:** from the worktree, `PYTHONPATH="src;D:/CodeD/grade9v4/workspace/test-tools" python -m pytest -q -p no:cacheprovider`. Compare pass count with A1's claim. Baseline: 2 known Windows symlink failures (WinError 1314); anything else is new.
3. **Privacy (public repo):** scan the PR diff for exam or textbook question text, answer keys, solution steps, scans/images, Drive links/ids, private paths. Flag any hit as STOP.
4. **Untouched originals:** the corrected reader `workspace/output/WPE_Core2_Reader_Fix_R1_20261031/rendered/core2.html` and the native bank are unchanged (hash before/after).
5. **Claim match:** each "done" item in A1's reply maps to a real file or test; list any claim with no artifact.
6. **Stacking:** which earlier open PR it builds on; whether it duplicates an earlier one.

## Result format (≤200 words)
```
RETURN <R##> · PR #<N> @<sha8> · ZIP <name> <sha8>
tests: <pass>/<fail> (claimed <n>) · new failures: <none|list>
privacy: CLEAN | STOP <what, where>
originals untouched: YES | NO
claims without artifact: <none|list>
needs physics/source review: <none|items>
NOT_RUN: <list>
```
