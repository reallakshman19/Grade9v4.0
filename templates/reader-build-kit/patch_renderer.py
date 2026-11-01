"""Apply the 'hints first' change to R3's private copy of render_core.py only (candidate change to Shared, not installed).

Owner decisions: "Yes, hints first" then "Allow before attempt": hints usable any time, one rung per click; the full working only after an attempt AND its own button. Each edit is an exact, asserted replacement.
"""
from pathlib import Path
import difflib, hashlib

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'runtime/Shared/tools/render_core.py'
ORIGINAL_SHA = '0ec1acc79750f24af2000adeb2549068414032ddcc72347b4bae97551fcceb06'

EDITS = [
    # 2. Core2 hints: usable before the attempt (Owner: "Allow before attempt"), opened one rung at a time.
    ('    return (secondary_disclosure(\n'
     '        "Need a hint? · guided support",\n'
     '        \'<div class="g9-eyebrow">Hint ladder · reveal only what you need</div>\' + lanes,\n'
     '        "core2-hints",\n'
     '    ) if lanes else "")',
     '    return (secondary_disclosure(\n'
     '        "Need a hint? · one at a time",\n'
     '        \'<div class="g9-eyebrow">Hint ladder · reveal only what you need</div>\' + lanes,\n'
     '        "core2-hints",\n'
     '    ) if lanes else "")'),
    # 3. The common wrong route moves out of its own early reveal ...
    ('            "TRAP": part("TRAP", reveal(\n'
     '                "Common wrong route · after your attempt",\n'
     '                block("common_wrong_route", \'<p>\' + question_text(ctx, q, "common_wrong_route", wrong_route) + \'</p>\'\n'
     '                      if isinstance(wrong_route, str) and wrong_route.strip() else "", title="Common wrong route"),\n'
     '                ref=f"CORE2-{rid}-wrong-route",\n'
     '            )),\n',
     '            # Hints first (Owner decision): the wrong route is part of the full answer, not an early reveal.\n'
     '            "TRAP": part("TRAP", ""),\n'),
    # 4. ... into the single full-answer reveal, which gets a clear button label.
    ('            "SOLUTION": part("SOLUTION", reveal("Answer and working", worked + teaching_figure + detailed_labels\n',
     '            "SOLUTION": part("SOLUTION", reveal("Show full answer and working", worked\n'
     '                             + block("common_wrong_route", \'<p>\' + question_text(ctx, q, "common_wrong_route", wrong_route) + \'</p>\'\n'
     '                                     if isinstance(wrong_route, str) and wrong_route.strip() else "", title="Common wrong route")\n'
     '                             + teaching_figure + detailed_labels\n'),
    # 5. Save whether the hint panel and the full answer are open ...
    ("const reveals=q('details[data-g9-support-reveal]',a).map(d=>!!d.open);const assistance=assistanceOf(a);"
     "store.set(key,JSON.stringify({attempted:!!a.dataset.attempted,assisted:!!a.dataset.g9Assisted,assistance,fields,ladders,reveals}))}",
     "const reveals=q('details[data-g9-support-reveal]',a).map(d=>!!d.open);const assistance=assistanceOf(a);"
     "const hints=!!hintPanel(a)?.open,full=!!fullAnswer(a)?.open;"
     "store.set(key,JSON.stringify({attempted:!!a.dataset.attempted,assisted:!!a.dataset.g9Assisted,assistance,fields,ladders,reveals,hints,full}))}\n"
     "function hintPanel(a){return q('details[data-g9-secondary=\"core2-hints\"]',a)[0]}\n"
     "function fullAnswer(a){return q('details[data-g9-payload-ref$=\"-solution\"]',a)[0]}"),
    # 6. ... restore them on reload (hint panel always; full answer only after a saved attempt) ...
    ("if(state.attempted){a.dataset.attempted='1';materialise(a)}lock()}",
     "if(state.attempted){a.dataset.attempted='1';materialise(a)}lock();"
     "{const h=hintPanel(a),f=fullAnswer(a);if(h)h.open=!!state.hints;if(f&&state.attempted)f.open=!!state.full}}"),
    # 7. ... and save on every open/close of either.
    ("q('details[data-g9-payload-ref$=\"-wrong-route\"]',a).forEach(d=>d.addEventListener('toggle',()=>{if(d.open){markAssistance(a,'WRONG_ROUTE');saveCore2State(a)}}));",
     "q('details[data-g9-payload-ref$=\"-wrong-route\"]',a).forEach(d=>d.addEventListener('toggle',()=>{if(d.open){markAssistance(a,'WRONG_ROUTE');saveCore2State(a)}}));"
     "[hintPanel(a),fullAnswer(a)].forEach(d=>d&&d.addEventListener('toggle',()=>saveCore2State(a)));"),
]

text = TARGET.read_text(encoding='utf-8')
before = text
assert hashlib.sha256(text.encode('utf-8')).hexdigest() == ORIGINAL_SHA, 'renderer copy is not the R1/R2 bytes'
for old, new in EDITS:
    assert text.count(old) == 1, ('edit anchor not unique', old[:80], text.count(old))
    text = text.replace(old, new)
TARGET.write_text(text, encoding='utf-8')
diff = ''.join(difflib.unified_diff(before.splitlines(True), text.splitlines(True),
                                    'canonical/Shared/tools/render_core.py', 'R3/runtime/Shared/tools/render_core.py'))
(ROOT / 'review/render_core.diff').write_text(diff, encoding='utf-8')
print('patched', hashlib.sha256(text.encode('utf-8')).hexdigest(), 'diff lines', diff.count('\n'))
