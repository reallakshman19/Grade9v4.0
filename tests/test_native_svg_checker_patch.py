"""Synthetic transform/entity negative controls for exact Owner-local Shared SVG patch.

Original textbook/exam figures are never copied into this public repository.
"""
import hashlib
import json
import xml.etree.ElementTree as ET
import re

import pytest

from grade9qa import native_svg_checker_patch as patch


def judge(svg, col=500, floor=12):
    ns={"ET":ET,"re":re}
    exec(patch.REPLACEMENT,ns)
    return ns["_figure_text_findings"](svg,col,floor)


def svg(body,viewbox='0 0 600 350'):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+viewbox+'">'+body+'</svg>'


def test_numeric_entities_are_decoded_before_width_estimation():
    # Many digits in an escaped entity are not separate rendered glyphs.
    label="Synthetic figure with arrow &#8658; result and &#956; work"
    s=svg(f'<text x="300" y="200" text-anchor="middle" font-size="16">{label}</text>')
    assert judge(s)==[]


def test_entity_decoding_does_not_suppress_true_clip():
    s=svg('<text x="598" y="200" font-size="18">&#956; work</text>')
    assert any("outside the viewBox" in item for item in judge(s))


def test_parent_translate_rotate_is_applied_to_local_negative_x():
    s=svg('<g transform="translate(240,160) rotate(-37)">'
          '<text x="-135" y="-10" font-size="18">&#956;R</text></g>')
    assert judge(s)==[]


def test_rotated_label_true_outside_is_still_reported():
    s=svg('<g transform="translate(590,160) rotate(-37)">'
          '<text x="40" y="0" font-size="18">SYNTHETIC TEST</text></g>')
    assert any("outside the viewBox" in item for item in judge(s))


def test_order_of_ancestor_transforms_is_respected():
    s=svg('<g transform="translate(230,143) rotate(-37)"><text x="0" y="-20"'
          ' text-anchor="middle" font-size="16">4 kg</text></g>')
    assert judge(s)==[]


def test_composite_matrix_translation_is_supported():
    s=svg('<g transform="matrix(1,0,0,1,240,160)">'
          '<text x="0" y="0" font-size="18">SYNTH</text></g>')
    assert judge(s)==[]


def test_nested_scale_with_inside_bbox():
    s=svg('<g transform="translate(120,80)"><g transform="scale(2)">'
          '<text x="10" y="20" font-size="18">SYNTH</text></g></g>')
    assert judge(s)==[]


def test_font_size_floor_warning_retained_independent_of_clipping():
    s=svg('<text x="200" y="200" font-size="8">SYNTH</text>')
    notes=judge(s,col=400,floor=12)
    assert any("smallest label" in item for item in notes)
    assert not any("outside the viewBox" in item for item in notes)


def test_unsupported_skew_does_not_silently_pass():
    s=svg('<g transform="skewX(20)"><text x="100" y="200" font-size="16">SYNTH</text></g>')
    assert any("requires browser/author review" in item for item in judge(s))


def test_complex_tspan_does_not_silently_pass():
    s=svg('<text x="100" y="200" font-size="16">A<tspan dx="20">B</tspan></text>')
    assert any("requires browser/author review" in item for item in judge(s))


def test_missing_x_does_not_silently_pass():
    s=svg('<text y="200" font-size="16">SYNTH</text>')
    assert any("requires browser/author review" in item for item in judge(s))


def test_invalid_svg_or_viewbox_requires_review():
    assert any("requires browser/author review" in item for item in judge('<svg><text>S</text></svg>'))
    assert any("requires browser/author review" in item for item in judge(svg('<text x="2" y="3">S</text>',viewbox='0 0 -600 300')))


def test_nonfinite_transform_is_not_trusted():
    s=svg('<g transform="translate(1e1000,0)"><text x="1" y="10">SYNTH</text></g>')
    assert any("requires browser/author review" in item for item in judge(s))


def test_original_renderer_exact_sha_mismatch_fails():
    with pytest.raises(ValueError,match="BYTE_PIN_MISMATCH"):
        patch.patch_original_renderer(b"this is not the owner Shared source")


def test_synthetic_original_anchored_patch_changes_only_checker(monkeypatch):
    synthetic=("import re\nimport xml.etree.ElementTree as ET\n"
               "class Ctx: pass\n"
               +patch.START+"\n    return ['OLD']\n\n"+
               patch.END+"\n    return None\n")
    monkeypatch.setattr(patch,"ORIGINAL_RENDERER_SHA256",hashlib.sha256(synthetic.encode()).hexdigest())
    result=patch.patch_original_renderer(synthetic.encode()).decode()
    assert patch.START in result
    assert "return ['OLD']" not in result
    assert patch.END in result
    assert "class Ctx: pass" in result
    compile(result,"candidate.py","exec")


def test_output_cannot_overwrite_owner_file(tmp_path):
    src=tmp_path/"owner.py";src.write_text("owner unchanged")
    with pytest.raises(ValueError,match="CANNOT_OVERWRITE"):
        patch.patch_to_private_file(src,src)
    assert src.read_text()=="owner unchanged"


def test_candidate_report_holds_academic_and_native(monkeypatch,tmp_path):
    synthetic=("import re\nimport xml.etree.ElementTree as ET\nclass Ctx: pass\n"
               +patch.START+"\n    return []\n\n"+
               patch.END+"\n    return None\n")
    monkeypatch.setattr(patch,"ORIGINAL_RENDERER_SHA256",hashlib.sha256(synthetic.encode()).hexdigest())
    original=tmp_path/"original.py";original.write_text(synthetic)
    out=tmp_path/"candidate.py"
    report=patch.patch_to_private_file(original,out)
    assert report["academic_status"]==report["release_status"]=="HOLD"
    assert report["native_shared_clearance"]=="NOT_PERFORMED"
    assert report["original_source_unchanged"] is True
    assert original.read_text()==synthetic
    assert out.read_text()!=synthetic
