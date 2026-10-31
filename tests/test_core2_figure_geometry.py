"""Synthetic source-independent tests for actual 4-figure/6-authoring receipt triage."""
import copy
import json

import pytest

from grade9qa.core2_figure_geometry import (
    PRODUCT, DIGEST, FIGURES, ABSENT_REPRESENTATIONS,
    original_receipt_identity, summarize, run,
)


def html():
    tags=''.join('<article data-g9-unit="SYNTH-%s"></article>' % i for i in range(9))
    return ('<html data-g9-role="CORE2" data-g9-product="'+PRODUCT+
            '" data-g9-render-digest="'+DIGEST+'">'+tags+'</html>')


def receipt():
    return {"renderer":"render_core/2","digest":DIGEST,"mode":"PAGES",
            "held_to":"REFERENCE","draft":True,
            "gaps":(
                [{"duty":"AUTHOR_COMPONENT","record":r,"component":"REPRESENTATION"} for r in ABSENT_REPRESENTATIONS]
                + [{"duty":"AUTHOR_FIGURE_TEXT","record":f,"component":"REPRESENTATION"} for f in FIGURES]
            )}


def good_geom():
    return {
        name: {
            "viewbox":{"x":0,"y":0,"width":600,"height":400},
            "label_count":5,"minimum_margin_native_units":5.5,
            "clipped_label_indices":[],"geometry_inside_viewbox":True,
        } for name in FIGURES
    }


def codes(result):
    return set(result["diagnostic_codes"])


def test_correct_original_receipt_geometry_is_not_a_waiver():
    result=summarize(html(),receipt(),good_geom())
    assert result["mechanical_status"]=="HOLD"
    assert result["figure_gap_disposition"]=="BROWSER_VS_HEURISTIC_DISCREPANCY_NOT_WAIVED"
    assert result["academic_status"]==result["release_status"]=="HOLD"
    assert result["native_shared_clearance"]=="NOT_PERFORMED"
    assert len(result["browser_results"])==4
    assert len(result["original_missing_representation_components"])==6


def test_real_clipping_fail_not_suppressed():
    geometry=good_geom()
    geometry[FIGURES[0]]["minimum_margin_native_units"]=-13
    geometry[FIGURES[0]]["clipped_label_indices"]=[1]
    geometry[FIGURES[0]]["geometry_inside_viewbox"]=False
    result=summarize(html(),receipt(),geometry)
    assert result["mechanical_status"]=="FAIL"
    assert "POTENTIAL_REAL_SVG_LABEL_CLIPPING" in codes(result)


def test_original_html_wrong_digest_fails():
    result=summarize(html().replace(DIGEST,"WRONG"),receipt(),good_geom())
    assert result["mechanical_status"]=="FAIL"
    assert any(c.startswith("NATIVE_HTML_DATA_G9_RENDER_DIGEST") for c in codes(result))


def test_wrong_original_receipt_gaps_not_auto_forgiven():
    r=receipt()
    r["gaps"]=r["gaps"][:-1]
    result=summarize(html(),r,good_geom())
    assert result["mechanical_status"]=="FAIL"
    assert "TEN_RENDER_GAPS_NOT_PRESERVED" in codes(result)


def test_absent_representation_cannot_be_omitted():
    r=receipt()
    r["gaps"][0]["record"]="SYNTHETIC_SWAP"
    result=summarize(html(),r,good_geom())
    assert result["mechanical_status"]=="FAIL"
    assert "ORIGINAL_SIX_AUTHOR_COMPONENT_FINDINGS_CHANGED" in codes(result)


def test_original_nine_cards_preserved():
    bad=html().replace('<article data-g9-unit="SYNTH-0"></article>', '')
    assert "ORIGINAL_NINE_QUESTION_CARD_COUNT_CHANGED" in codes(summarize(bad,receipt(),good_geom()))


def test_missing_figure_measurement_fails_closed():
    geometry=good_geom()
    geometry.pop(FIGURES[2])
    result=summarize(html(),receipt(),geometry)
    assert result["mechanical_status"]=="FAIL"
    assert "NOT_ALL_FOUR_ORIGINAL_FIGURES_MEASURED" in codes(result)


def test_empty_or_nonfinite_witness_rejected():
    geometry=good_geom()
    geometry[FIGURES[0]]["minimum_margin_native_units"]=float("nan")
    assert "INVALID_BROWSER_FIGURE_WITNESS" in codes(summarize(html(),receipt(),geometry))


def test_source_text_never_echoed_into_browser_report():
    original=html()+"PRIVATE_EXAM_STEM"
    r=receipt();r["private_original_worked_answer"]="PRIVATE_WORKED_ANSWER"
    g=good_geom();g[FIGURES[0]]["private_text"]="PRIVATE_FIGURE_CAPTION"
    report=json.dumps(summarize(original,r,g))
    assert "PRIVATE_EXAM" not in report
    assert "PRIVATE_WORKED" not in report
    assert "PRIVATE_FIGURE" not in report


def test_original_html_not_overwritten_by_audit(tmp_path):
    original=tmp_path/"original.html"
    receipt_path=tmp_path/"render-receipt.json"
    original.write_text(html())
    receipt_path.write_text(json.dumps(receipt()))
    with pytest.raises(ValueError, match="CANNOT_OVERWRITE"):
        run(original,receipt_path,original)


def test_missing_browser_evidence_stays_hold_not_pass():
    result=summarize(html(),receipt(),None)
    assert result["academic_status"]=="HOLD"
    assert result["mechanical_status"]=="FAIL"
    assert "CHROMIUM_GEOMETRY_WITNESS_NOT_PROVIDED" in codes(result)
