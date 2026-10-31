"""Metadata-only browser geometry evidence for original Owner Core2 SVG figures.

The original Shared renderer's AUTHOR_FIGURE_TEXT warning uses textual width
estimates without SVG transform matrices. Chromium measures actual transformed
text bounds. A browser geometry check is NOT a native Shared waiver, academic
approval, print QA, tablet readability approval, or source figure correction.

Only exact existing native Core2 receipt identities are supported. The six
source-authored REPRESENTATION omissions cannot be fixed by editing HTML.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

PRODUCT = "WPE-CORE2-NATIVE-INTEGRATION-R1"
DIGEST = "a13a70605acf789d"
FIGURES = (
    "REP-TB-FIG-06-INCLINE-BLOCK",
    "REP-TB-FIG-07-INCLINE-FBD",
    "REP-TB-FIG-09-OVERHANGING-CHAIN",
    "REP-TB-FIG-10-SPRING-BLOCK-WALL",
)
ABSENT_REPRESENTATIONS = (
    "TB-WPE-ILL-01", "TB-WPE-ILL-02", "TB-WPE-ILL-03",
    "TB-WPE-ILL-05", "TB-WPE-ILL-06", "TB-WPE-ILL-11",
)


def original_receipt_identity(html: str, receipt: dict) -> list[str]:
    problems = []
    if not isinstance(receipt, dict) or receipt.get("renderer") != "render_core/2":
        problems.append("ORIGINAL_RENDERER_RECEIPT_INVALID")
        return problems
    if receipt.get("digest") != DIGEST or receipt.get("mode") != "PAGES":
        problems.append("RENDER_RECEIPT_DIGEST_OR_MODE_MISMATCH")
    if receipt.get("draft") is not True or receipt.get("held_to") != "REFERENCE":
        problems.append("NON_DRAFT_NATIVE_RECEIPT_NOT_SUPPORTED")
    root = re.search(r"<html\b[^>]+>", html, re.I)
    head = root.group() if root else ""
    for key, val in (("data-g9-role", "CORE2"), ("data-g9-product", PRODUCT),
                     ("data-g9-render-digest", DIGEST)):
        if not re.search(r'\b' + re.escape(key) + r'="' + re.escape(val) + r'"', head):
            problems.append("NATIVE_HTML_" + key.upper().replace("-", "_") + "_MISMATCH")
    if len(re.findall(r"<article\b[^>]+\bdata-g9-unit=", html)) != 9:
        problems.append("ORIGINAL_NINE_QUESTION_CARD_COUNT_CHANGED")
    gaps = receipt.get("gaps")
    if not isinstance(gaps, list) or len(gaps) != 10:
        problems.append("TEN_RENDER_GAPS_NOT_PRESERVED")
        return problems
    observed_figure = {x.get("record") for x in gaps if isinstance(x, dict) and
                       x.get("duty") == "AUTHOR_FIGURE_TEXT"}
    observed_rep = {x.get("record") for x in gaps if isinstance(x, dict) and
                    x.get("duty") == "AUTHOR_COMPONENT" and x.get("component") == "REPRESENTATION"}
    if observed_figure != set(FIGURES):
        problems.append("ORIGINAL_FOUR_FIGURE_FINDINGS_CHANGED")
    if observed_rep != set(ABSENT_REPRESENTATIONS):
        problems.append("ORIGINAL_SIX_AUTHOR_COMPONENT_FINDINGS_CHANGED")
    return problems


def browser_measurements(page) -> dict:
    """Run on isolated Owner-local original HTML loaded into Chromium.

    Original draft's *author-only* reveal helper is used to inspect native
    figures inside post-attempt templates; this is not a learner attempt test.
    No original HTML, original question content or screenshots are emitted.
    """
    results = {}
    before = page.evaluate("""() => ({
      solutionFbdInLiveDom: !!document.querySelector('figure[data-g9-representation="REP-TB-FIG-07-INCLINE-FBD"]'),
      chainInLiveDom: !!document.querySelector('figure[data-g9-representation="REP-TB-FIG-09-OVERHANGING-CHAIN"]')
    })""")
    if before["solutionFbdInLiveDom"] or before["chainInLiveDom"]:
        raise ValueError("SOLUTION_ONLY_FIGURES_PRESENT_BEFORE_AUTHOR_REVEAL")
    if not page.evaluate("typeof window.g9MaterialiseAll === 'function'"):
        raise ValueError("ORIGINAL_AUTHOR_PREVIEW_HOOK_NOT_AVAILABLE")
    page.evaluate("window.g9MaterialiseAll()")
    for figure in FIGURES:
        record = page.evaluate("""rep => {
            const fig = [...document.querySelectorAll('figure[data-g9-representation]')]
                        .find(el => el.dataset.g9Representation === rep);
            const svg = fig?.querySelector('svg');
            if (!svg || !svg.getScreenCTM()) return null;
            const vb = svg.viewBox.baseVal;
            const viewbox = {x:vb.x,y:vb.y,width:vb.width,height:vb.height};
            const inverse = svg.getScreenCTM().inverse();
            const labels = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim());
            const margins = [], clipped = [];
            for(const node of labels) {
                if (!node.getScreenCTM()) return {error:"TEXT_MATRIX_MISSING"};
                const box = node.getBBox();
                const matrix = inverse.multiply(node.getScreenCTM());
                const pts = [[box.x,box.y],[box.x+box.width,box.y],
                             [box.x+box.width,box.y+box.height],[box.x,box.y+box.height]]
                      .map(([x,y]) => ({x:matrix.a*x+matrix.c*y+matrix.e,
                                         y:matrix.b*x+matrix.d*y+matrix.f}));
                const left=Math.min(...pts.map(x=>x.x)), right=Math.max(...pts.map(x=>x.x));
                const top=Math.min(...pts.map(x=>x.y)), bottom=Math.max(...pts.map(x=>x.y));
                const margin=Math.min(left-vb.x,vb.x+vb.width-right,top-vb.y,vb.y+vb.height-bottom);
                if(!Number.isFinite(margin))return {error:"NONFINITE_TEXT_GEOMETRY"};
                margins.push(margin);
                if(margin < -0.05) clipped.push({index:labels.indexOf(node),margin});
            }
            return {viewbox,label_count:labels.length,
                    minimum_margin_native_units:margins.length?Math.min(...margins):null,
                    clipped_label_indices:clipped.map(x=>x.index),
                    geometry_inside_viewbox:labels.length>0&&clipped.length===0};
        }""", figure)
        if not isinstance(record, dict) or record.get("error"):
            raise ValueError("BROWSER_GEOMETRY_MEASUREMENT_INVALID")
        results[figure] = record
    return results


def summarize(original_html: str, original_receipt: dict,
              geometries: dict | None, *, html_sha256: str | None = None,
              receipt_sha256: str | None = None) -> dict:
    problems = original_receipt_identity(original_html, original_receipt)
    results = []
    if geometries is None:
        problems.append("CHROMIUM_GEOMETRY_WITNESS_NOT_PROVIDED")
        geometries = {}
    for figure in FIGURES:
        row = geometries.get(figure)
        if not isinstance(row, dict):
            problems.append("MISSING_BROWSER_FIGURE_WITNESS")
            continue
        box = row.get("viewbox")
        margin = row.get("minimum_margin_native_units")
        label_count = row.get("label_count")
        if (not isinstance(box, dict) or not all(type(box.get(n)) in (int,float) for n in ("x","y","width","height"))
                or box.get("width",0)<=0 or box.get("height",0)<=0
                or type(label_count) is not int or label_count<1
                or type(margin) not in (int,float) or not -1e7 < margin < 1e7):
            problems.append("INVALID_BROWSER_FIGURE_WITNESS")
            continue
        inside = (row.get("geometry_inside_viewbox") is True and margin>=-0.05
                  and row.get("clipped_label_indices")==[])
        if not inside:
            problems.append("POTENTIAL_REAL_SVG_LABEL_CLIPPING")
        results.append({
            "figure_id":figure,
            "browser_label_count":label_count,
            "minimum_transformed_margin_native_units":round(margin,2),
            "browser_geometry": "INSIDE_VIEWBOX" if inside else "POTENTIAL_CLIPPING",
            "native_reference_warning": "AUTHOR_FIGURE_TEXT",
            "source_figure_modified":False,
            "native_receipt_waived":False,
        })
    if len(results)!=4:
        problems.append("NOT_ALL_FOUR_ORIGINAL_FIGURES_MEASURED")
    problems += ["SIX_NATIVE_REPRESENTATION_COMPONENTS_NOT_AUTHORED",
                 "ORIGINAL_RENDERER_WARNING_REQUIRES_NATIVE_SOURCE_REVIEW",
                 "REFERENCE_TABLET_READABILITY_AND_PRINT_NOT_PROVEN",
                 "STATIC_HTML_ANSWER_CUSTODY_AND_RELEASE_NOT_PROVEN"]
    critical = {"ORIGINAL_RENDERER_RECEIPT_INVALID","RENDER_RECEIPT_DIGEST_OR_MODE_MISMATCH",
                "NON_DRAFT_NATIVE_RECEIPT_NOT_SUPPORTED","TEN_RENDER_GAPS_NOT_PRESERVED",
                "ORIGINAL_FOUR_FIGURE_FINDINGS_CHANGED","ORIGINAL_SIX_AUTHOR_COMPONENT_FINDINGS_CHANGED",
                "ORIGINAL_NINE_QUESTION_CARD_COUNT_CHANGED",
                "INVALID_BROWSER_FIGURE_WITNESS","MISSING_BROWSER_FIGURE_WITNESS",
                "NOT_ALL_FOUR_ORIGINAL_FIGURES_MEASURED","POTENTIAL_REAL_SVG_LABEL_CLIPPING"}
    mechanical = "FAIL" if any(x in critical or x.startswith("NATIVE_HTML_") for x in problems) else "HOLD"
    return {
        "schema_version":"1.0.0",
        "audit_type":"ORIGINAL_NATIVE_CORE2_BROWSER_FIGURE_TEXT_GEOMETRY",
        "product_id":PRODUCT,
        "original_render_digest":DIGEST,
        "original_html_sha256":html_sha256,
        "original_render_receipt_sha256":receipt_sha256,
        "original_receipt_gap_count":10,
        "original_missing_representation_components":list(ABSENT_REPRESENTATIONS),
        "original_figure_warning_ids":list(FIGURES),
        "browser_results":results,
        "mechanical_status":mechanical,
        "figure_gap_disposition": "BROWSER_VS_HEURISTIC_DISCREPANCY_NOT_WAIVED",
        "missing_representation_status": "SIX_UNAUTHORED_SOURCE_COMPONENTS_HOLD",
        "academic_status":"HOLD","native_shared_clearance":"NOT_PERFORMED",
        "release_status":"HOLD",
        "diagnostic_codes":sorted(set(problems)),
        "warning":"Browser bounding-box checks do not amend native authored SVG source, waive a renderer gap, authenticate source accuracy, or prove physical label readability.",
    }


def run(original_html: Path, original_receipt: Path, out: Path,
        *, chromium_executable: str | None = None) -> dict:
    original_html = Path(original_html).resolve()
    original_receipt = Path(original_receipt).resolve()
    out = Path(out).resolve()
    if out in {original_html, original_receipt}:
        raise ValueError("CANNOT_OVERWRITE_OWNER_ORIGINAL")
    raw_html = original_html.read_bytes()
    raw_receipt = original_receipt.read_bytes()
    html = raw_html.decode("utf8")
    receipt = json.loads(raw_receipt)
    if original_receipt_identity(html, receipt):
        raise ValueError("ORIGINAL_CORE2_NATIVE_RECEIPT_DOES_NOT_MATCH_HTML")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("CHROMIUM_PLAYWRIGHT_REQUIRED_FOR_PRIVATE_BROWSER_AUDIT") from exc
    with sync_playwright() as playwright:
        opts = {"headless":True,"args":["--no-sandbox"]}
        if chromium_executable:
            opts["executable_path"] = chromium_executable
        browser = playwright.chromium.launch(**opts)
        try:
            page = browser.new_page(viewport={"width":1280,"height":850})
            page.set_content(html, wait_until="domcontentloaded")
            geometry=browser_measurements(page)
        finally:
            browser.close()
    report=summarize(html, receipt, geometry,
                     html_sha256=hashlib.sha256(raw_html).hexdigest(),
                     receipt_sha256=hashlib.sha256(raw_receipt).hexdigest())
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description="Private existing native Core2 SVG diagnostic, never a Shared waiver")
    p.add_argument("--original-html",required=True)
    p.add_argument("--original-receipt",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--chromium",default=None)
    args=p.parse_args(argv)
    r=run(args.original_html,args.original_receipt,args.out,chromium_executable=args.chromium)
    print("CORE2-SVG-GEOMETRY mechanical="+r["mechanical_status"]+" academic=HOLD native-waiver=NOT_PERFORMED")
    return 1 if r["mechanical_status"]=="FAIL" else 3


if __name__=="__main__":
    raise SystemExit(main())
