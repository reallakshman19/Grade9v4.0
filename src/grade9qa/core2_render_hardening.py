"""Fail-closed patch for Owner-local native Shared render_core/2.

Does not publish the original renderer or any question content. Patches only
Core2 role JS, preserving generic JS and Core1B's exact-match specializations.
A new native rendering/receipt, source review and server-side answer custody
remain separate requirements; this is a private draft browser safety patch.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

OLD_SAVE = "function saveCore2State(a){if(a.dataset.g9Role!=='CORE2')return;const key=stateKey(a);if(!key)return;const fields=attemptFields(a).map(el=>({value:el.value,checked:!!el.checked}));const ladders={};q('.g9-ladder[data-g9-ladder-ref]',a).forEach(l=>ladders[l.dataset.g9LadderRef]=rungCount(l));const reveals=q('details[data-g9-support-reveal]',a).map(d=>!!d.open);const assistance=assistanceOf(a);store.set(key,JSON.stringify({attempted:!!a.dataset.attempted,assisted:!!a.dataset.g9Assisted,assistance,fields,ladders,reveals}))}"
NEW_SAVE = "function saveCore2State(a,commit=false){if(a.dataset.g9Role!=='CORE2')return false;const key=stateKey(a);if(!key)return false;const fields=attemptFields(a).map(el=>({value:el.value,checked:!!el.checked}));const ladders={};q('.g9-ladder[data-g9-ladder-ref]',a).forEach(l=>ladders[l.dataset.g9LadderRef]=rungCount(l));const reveals=q('details[data-g9-support-reveal]',a).map(d=>!!d.open);const assistance=assistanceOf(a);const state={attempted:commit||!!a.dataset.attempted,assisted:!!a.dataset.g9Assisted,assistance,fields,ladders,reveals};if(!store.set(key,JSON.stringify(state)))return false;const saved=readState(key);return !!saved&&saved.attempted===state.attempted&&JSON.stringify(saved.fields)===JSON.stringify(state.fields)}"
OLD_COMMIT = "q('[data-g9-commit]',a).forEach(b=>b.onclick=()=>{const box=b.closest('[data-g9-attempt-box]');if(!box||!validAttempt(box)){q('input,textarea,select',box||a)[0]?.focus();return}a.dataset.attempted='1';lock();materialise(a);saveCore2State(a)});"
NEW_COMMIT = "q('[data-g9-commit]',a).forEach(b=>b.onclick=()=>{const box=b.closest('[data-g9-attempt-box]');if(a.dataset.attempted)return;if(!box||!validAttempt(box)){q('input,textarea,select',box||a)[0]?.focus();return}if(!saveCore2State(a,true)){a.dataset.g9SaveFailure='1';b.setAttribute('aria-invalid','true');b.title='Response not saved. Check browser storage and retry.';b.textContent='Response not saved — retry';return}delete a.dataset.g9SaveFailure;b.removeAttribute('aria-invalid');a.dataset.attempted='1';lock();materialise(a);b.disabled=true});"
OLD_DEBUG = "window.g9MaterialiseAll=()=>articles.forEach(a=>{a.dataset.attempted='1';q('details[data-requires-attempt]',a).forEach(d=>delete d.dataset.locked);materialise(a);q('.g9-ladder',a).forEach(l=>{while(nextRung(l)){};});q('details[data-g9-support-reveal]',a).forEach(d=>d.open=true)});"
NEW_DEBUG = "/* Core2 learner pages: no author-only g9MaterialiseAll reveal hook. */"
PATCHES = ((OLD_SAVE, NEW_SAVE), (OLD_COMMIT, NEW_COMMIT), (OLD_DEBUG, NEW_DEBUG))
RENDER_ANCHOR = "core1b_js() if role == 'CORE1B' else JS"
RENDER_NEW = "core1b_js() if role == 'CORE1B' else core2_js() if role == 'CORE2' else JS"
INJECT_ANCHOR = "def core1b_js() -> str:"

def patch_runtime_js(source: str) -> str:
    for before, after in PATCHES:
        if source.count(before) != 1:
            raise ValueError("CORE2_RUNTIME_ANCHOR_MISSING_OR_DUPLICATE")
        source = source.replace(before, after, 1)
    return source

def patch_native_source(source: str) -> str:
    if source.count(RENDER_ANCHOR) != 1 or source.count(INJECT_ANCHOR) != 1:
        raise ValueError("NATIVE_SHARED_RENDERER_REVISION_NOT_SUPPORTED")
    function = ('def core2_js() -> str:\n'
                '    """Core2 only: verify persistence before answer materialization."""\n'
                '    js = JS\n'
                '    patches = ' + repr(PATCHES) + '\n'
                '    for before, after in patches:\n'
                '        if js.count(before) != 1:\n'
                '            raise ValueError("CORE2_RUNTIME_PATCH_UNSAFE")\n'
                '        js = js.replace(before, after, 1)\n'
                '    return js\n\n\n')
    return source.replace(INJECT_ANCHOR, function + INJECT_ANCHOR, 1).replace(RENDER_ANCHOR, RENDER_NEW, 1)

def patch_private_html(source: str) -> str:
    if ('data-g9-role="CORE2"' not in source or
            'data-g9-render-digest="' not in source or
            'data-g9-product="' not in source):
        raise ValueError("NATIVE_CORE2_HTML_IDENTITY_NOT_PRESENT")
    return patch_runtime_js(source)

def write_candidate(original: Path, output: Path, kind: str) -> dict:
    original, output = original.resolve(), output.resolve()
    if original == output:
        raise ValueError("CANNOT_MODIFY_ORIGINAL_OWNER_FILE")
    if kind not in ("renderer", "private_html"):
        raise ValueError("PATCH_KIND_UNSUPPORTED")
    if kind == "renderer":
        for parent in original.parents:
            if parent.name == "Shared" and output.is_relative_to(parent):
                raise ValueError("CANNOT_WRITE_INSIDE_ORIGINAL_SHARED_ROOT")
    before = original.read_bytes()
    text = before.decode("utf-8")
    patched = patch_native_source(text) if kind == "renderer" else patch_private_html(text)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(patched, encoding="utf-8")
    after = output.read_bytes()
    return {
        "kind": kind,
        "original_sha256": hashlib.sha256(before).hexdigest(),
        "candidate_sha256": hashlib.sha256(after).hexdigest(),
        "original_bytes": len(before), "candidate_bytes": len(after),
        "native_render_receipt": "NOT_REGENERATED",
        "academic_status": "HOLD", "learner_release": "HOLD",
        "warning": "Client-localStorage attempt safety only; original HTML includes answer templates. Independent server-side answer custody and author-review remain HOLD."
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description="Owner-local candidate native Core2 patch, no approval")
    parser.add_argument("--kind", required=True, choices=("renderer", "private_html"))
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args(argv)
    inp, out, receipt = [Path(v).resolve() for v in (args.input, args.out, args.receipt)]
    if len({inp, out, receipt}) != 3:
        raise ValueError("INPUT_OUTPUT_RECEIPT_MUST_BE_DISTINCT")
    result = write_candidate(inp, out, args.kind)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("CORE2_NATIVE_RUNTIME candidate only; academic=HOLD release=HOLD")
    return 3

if __name__ == "__main__":
    raise SystemExit(main())
