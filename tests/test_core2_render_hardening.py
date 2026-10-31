"""No Owner content needed; exact-match patch safety and Core2-only role routing."""
import json
import pytest

from grade9qa.core2_render_hardening import (
    OLD_SAVE, OLD_COMMIT, OLD_RESTORE, OLD_DEBUG, NEW_SAVE, NEW_COMMIT, PATCHES,
    RENDER_ANCHOR, patch_runtime_js, patch_native_source, patch_private_html,
    write_candidate,
)


def runtime():
    return "\n".join([OLD_SAVE, OLD_COMMIT, OLD_RESTORE, OLD_DEBUG])


def native():
    return (
        "JS = " + repr(runtime()) + "\n"
        "def core1b_js() -> str:\n"
        "    return JS\n"
        "def render_page(role):\n"
        "    return " + RENDER_ANCHOR + "\n"
    )


def test_native_patch_preserves_core1b_original_runtime():
    ns = {}
    exec(compile(patch_native_source(native()), "<synthetic>", "exec"), ns)
    assert ns["render_page"]("CORE1B") == runtime()
    assert ns["render_page"]("CORE1") == runtime()
    assert ns["render_page"]("CORE2") == patch_runtime_js(runtime())


def test_core2_reveal_follows_verified_persistence():
    js = patch_runtime_js(runtime())
    assert "if(!saveCore2State(a,true))" in js
    assert js.index("if(!saveCore2State(a,true))") < js.index("a.dataset.attempted='1'")
    assert js.index("a.dataset.attempted='1'") < js.index("materialise(a)")


def test_readback_required_before_reveal():
    js = patch_runtime_js(runtime())
    assert "const saved=readState(key)" in js
    assert "JSON.stringify(saved.fields)===JSON.stringify(state.fields)" in js
    assert "Response not saved" in js


def test_core2_debug_materialise_hook_not_exposed():
    js = patch_runtime_js(runtime())
    assert "window.g9MaterialiseAll=" not in js


def test_unknown_renderer_version_fails_closed():
    with pytest.raises(ValueError):
        patch_native_source("JS='anything'; def other(): pass")


def test_duplicate_native_anchor_fails_closed():
    with pytest.raises(ValueError):
        patch_native_source(native() + "\n" + RENDER_ANCHOR)


def test_duplicate_runtime_anchors_fail_closed():
    with pytest.raises(ValueError):
        patch_runtime_js(runtime()+"\n"+OLD_SAVE)


def test_non_core2_html_not_patchable():
    with pytest.raises(ValueError):
        patch_private_html("<html data-g9-role='INDEX'><body></body></html>")


def test_matching_private_html_is_separate_candidate():
    html = '<html data-g9-role="CORE2" data-g9-product="SYNTH-ONLY" data-g9-render-digest="abc"><script>' + runtime() + '</script></html>'
    out = patch_private_html(html)
    assert out.startswith('<html data-g9-role="CORE2"')
    assert "g9MaterialiseAll=" not in out


def test_same_source_and_output_never_overwritten(tmp_path):
    p = tmp_path / "private.html"
    p.write_text('UNTOUCHED')
    with pytest.raises(ValueError):
        write_candidate(p,p,"private_html")
    assert p.read_text() == "UNTOUCHED"


def test_separate_output_retains_original_checksum_and_hold(tmp_path):
    original=tmp_path / "original.html"
    changed=tmp_path / "patched.html"
    original.write_text('<html data-g9-role="CORE2" data-g9-product="SYNTH-ONLY" data-g9-render-digest="abc"><script>'+runtime()+'</script></html>')
    orig=original.read_bytes()
    summary=write_candidate(original,changed,"private_html")
    assert original.read_bytes() == orig
    assert changed.exists()
    assert summary["academic_status"]==summary["learner_release"]=="HOLD"
    assert summary["native_render_receipt"]=="NOT_REGENERATED"
    assert "answer templates" in summary["warning"]
