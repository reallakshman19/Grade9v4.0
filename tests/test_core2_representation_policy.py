"""Synthetic fixtures only: original Shared EXPECTED waiver and protected figures."""
import hashlib
import json
import pytest

from grade9qa.core2_representation_policy import (
    PRODUCT, DIGEST, RECORDS, SOLUTION_FIGURES, inspect_original,
)


def fixture():
    cards=[]
    for name in (*RECORDS,"SYN-EXTRA-1","SYN-EXTRA-2","SYN-CONTROL"):
        solution=(f'<template data-g9-payload="SYNTH-{name}-solution">'
                  f'<figure data-g9-representation="{SOLUTION_FIGURES[name]}"></figure>'
                  '</template>') if name in SOLUTION_FIGURES else ""
        cards.append(f'<article data-g9-unit="{name}"><p>SYNTHETIC ONLY</p>{solution}</article>')
    html=(f'<html data-g9-role="CORE2" data-g9-product="{PRODUCT}" '
          f'data-g9-render-digest="{DIGEST}"><body>'+''.join(cards)+'</body></html>').encode()
    receipt=json.dumps({"renderer":"render_core/2","digest":DIGEST,"draft":True,
        "held_to":"REFERENCE","gaps":[
            *({"record":r,"duty":"AUTHOR_COMPONENT","component":"REPRESENTATION"} for r in RECORDS),
            *({"record":f"SYNTH-FIG-{i}","duty":"AUTHOR_FIGURE_TEXT"} for i in range(4)),
        ]}).encode()
    registry=json.dumps({"blueprints":[{"id":"BP-CORE2-SOURCE-QUESTION","version":"1.11.0","status":"ACTIVE",
        "core_roles":["CORE2"],
        "components":[{"id":"REPRESENTATION","level":"EXPECTED","min_items":1,
                       "authoring":{"hint":"Author a diagram or waive with reason."}}]}]}).encode()
    return html,receipt,registry


def inspect(items=None):
    h,r,b=fixture() if items is None else items
    return inspect_original(h,r,b,html_pin=hashlib.sha256(h).hexdigest(),
                            receipt_pin=hashlib.sha256(r).hexdigest(),
                            blueprint_pin=hashlib.sha256(b).hexdigest())


def test_six_record_review_proposal_counts_and_explicit_holds():
    x=inspect()
    assert x["native_component_level"]=="EXPECTED"
    assert x["waiver_proposals"]==3 and x["neutral_authoring_candidates"]==2
    assert x["source_physics_holds"]==1 and x["missing_representation_records"]==6
    assert x["academic_status"]==x["learner_release"]=="HOLD"
    assert x["shared_native_acceptance"]=="NOT_PERFORMED"
    assert all(t["native_waiver_applied"] is False and t["original_gap_status"]=="OPEN" for t in x["tickets"])


def test_original_nine_cards_and_ten_receipt_gaps_preserved():
    x=inspect()
    assert [t["question_id"] for t in x["tickets"]]==list(RECORDS)
    assert x["existing_native_cards"]==9 and x["original_receipt_gaps"]==10


def test_two_existing_figures_are_solution_only():
    x=inspect()
    assert all(t["existing_figure_evidence"][0]["phase"]=="POST_ATTEMPT_TEMPLATE"
               for t in x["tickets"] if t["question_id"] in SOLUTION_FIGURES)


def test_solution_figure_promoted_before_attempt_is_rejected():
    h,r,b=fixture()
    ref=SOLUTION_FIGURES["TB-WPE-ILL-02"]
    h=h.replace(f'<template data-g9-payload="SYNTH-TB-WPE-ILL-02-solution">'
                f'<figure data-g9-representation="{ref}"></figure></template>'.encode(),
                f'<figure data-g9-representation="{ref}"></figure>'.encode())
    with pytest.raises(ValueError,match="PREATTEMPT_FIGURE"):
        inspect((h,r,b))


def test_blueprint_required_instead_of_expected_fails_closed():
    h,r,b=fixture();b=b.replace(b'"EXPECTED"',b'"REQUIRED"')
    with pytest.raises(ValueError,match="NATIVE_REPRESENTATION_APPLICABILITY_CONTRACT_CHANGED"):
        inspect((h,r,b))


def test_blueprint_without_waiver_authoring_rule_fails_closed():
    h,r,b=fixture();b=b.replace(b"waive with reason",b"not a waiver")
    # Contract now still contains the word 'waive' in 'waiver'; use an unambiguous replacement.
    b=b.replace(b"not a waiver",b"mandatory and unwaivable")
    with pytest.raises(ValueError,match="NATIVE_REPRESENTATION_APPLICABILITY_CONTRACT_CHANGED"):
        inspect((h,r,b))


def test_six_original_component_gap_ids_must_match():
    h,r,b=fixture();r=r.replace(b"TB-WPE-ILL-01",b"SYN-ALTERED")
    with pytest.raises(ValueError,match="ORIGINAL_SIX_MISSING_REPRESENTATIONS_CHANGED"):
        inspect((h,r,b))


def test_native_nine_card_count_not_fabricated():
    h,r,b=fixture()
    h=h.replace(b'<article data-g9-unit="SYN-CONTROL"><p>SYNTHETIC ONLY</p></article>',b"")
    with pytest.raises(ValueError,match="ORIGINAL_NINE_CORE2_CARDS_CHANGED"):
        inspect((h,r,b))


def test_source_figure_reference_swap_fails():
    h,r,b=fixture();h=h.replace(b"REP-TB-FIG-09-OVERHANGING-CHAIN",b"REP-SYNTHETIC")
    with pytest.raises(ValueError,match="SOLUTION_ONLY_FIGURE_LEAK_OR_IDENTITY_CHANGED"):
        inspect((h,r,b))


def test_forged_receipt_approved_flags_not_trusted():
    h,r,b=fixture();data=json.loads(r)
    data["academic_status"]="APPROVED";data["release"]="APPROVED"
    x=inspect((h,json.dumps(data).encode(),b))
    assert x["academic_status"]=="HOLD" and x["original_receipt_modified"] is False


def test_source_original_words_not_leaked_in_metadata():
    h,r,b=fixture();h=h.replace(b"SYNTHETIC ONLY",b"PRIVATE_SOURCE_TEXT_NOT_PUBLIC")
    x=inspect((h,r,b))
    assert "PRIVATE_SOURCE_TEXT" not in json.dumps(x)


def test_wrong_original_html_sha_pin_rejected():
    h,r,b=fixture()
    with pytest.raises(ValueError,match="OWNER_HTML_EXACT_BYTE_PIN_MISMATCH"):
        inspect_original(h,r,b)


def test_output_cannot_replace_original_source_file(tmp_path):
    from grade9qa.core2_representation_policy import main
    f=tmp_path/"same";f.write_text("{}")
    with pytest.raises(ValueError,match="CANNOT_OVERWRITE_OWNER_ORIGINAL"):
        main(["--original-html",str(f),"--render-receipt",str(tmp_path/"other"),
              "--shared-web-blueprints",str(tmp_path/"bp"),"--out",str(f)])
