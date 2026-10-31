"""Owner-local candidate patch for original Shared render_core/2 SVG checker.

The original figure checker counts XML numeric character entities as multiple
characters and ignores nested SVG transforms when judging clipping. This
source-independent exact-anchor patch supplies a transform-aware approximation.
It preserves the separate minimum label-size warning, keeps unknown geometry
under review and does not alter any figures or source materials.

Requires independent Owner/Shared integration and an original native rebuild.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ORIGINAL_RENDERER_SHA256 = "0ec1acc79750f24af2000adeb2549068414032ddcc72347b4bae97551fcceb06"
START = "def _figure_text_findings(svg: str, column_px: float, minimum_px: float) -> list[str]:"
END = "\ndef _figure_column_px(ctx: Ctx, role: str) -> tuple[float, float] | None:"

REPLACEMENT = '''def _figure_text_findings(svg: str, column_px: float, minimum_px: float) -> list[str]:
    """Approximate *transformed* text bounds, not encoded-source character counts.

    Conservatively report unsupported/malformed SVG for independent browser
    inspection. These are advisory authoring checks, not a source fidelity or
    academic review, nor proof of true glyph bounds or mobile readability.
    """
    import math
    def fail(reason):
        return ["SVG text geometry requires browser/author review: " + reason]
    try:
        root = ET.fromstring(svg)
        if root.tag.rsplit("}", 1)[-1] != "svg":
            return fail("root is not SVG")
        viewbox = root.get("viewBox", "").replace(",", " ").split()
        if len(viewbox) != 4:
            return fail("missing or invalid viewBox")
        vx, vy, vw, vh = (float(x) for x in viewbox)
        if not all(math.isfinite(x) for x in (vx,vy,vw,vh)) or vw <= 0 or vh <= 0:
            return fail("nonfinite or nonpositive viewBox")
        if not all(math.isfinite(x) and x > 0 for x in (column_px, minimum_px)):
            return fail("invalid tablet geometry inputs")
        scale = column_px / vw
    except (ET.ParseError, ValueError, TypeError, OverflowError):
        return fail("cannot parse SVG geometry")

    def multiply(a, b):
        # SVG affine [a,b,c,d,e,f]: parent × child
        a0,b0,c0,d0,e0,f0=a
        a1,b1,c1,d1,e1,f1=b
        return (a0*a1+c0*b1,b0*a1+d0*b1,
                a0*c1+c0*d1,b0*c1+d0*d1,
                a0*e1+c0*f1+e0,b0*e1+d0*f1+f0)

    def transforms(value):
        result=(1.,0.,0.,1.,0.,0.)
        pos=0
        for found in re.finditer(r"([A-Za-z]+)\\s*\\(([^)]*)\\)", value):
            if value[pos:found.start()].strip(" ,\\t\\r\\n"):
                raise ValueError("malformed SVG transform")
            pos=found.end()
            name=found.group(1)
            nums=[float(x) for x in re.findall(r"[+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[Ee][+-]?\\d+)?",found.group(2))]
            if not all(math.isfinite(x) for x in nums):
                raise ValueError("nonfinite SVG transform")
            if name=="translate" and len(nums) in (1,2):
                m=(1.,0.,0.,1.,nums[0],nums[1] if len(nums)>1 else 0.)
            elif name=="scale" and len(nums) in (1,2):
                m=(nums[0],0.,0.,nums[1] if len(nums)>1 else nums[0],0.,0.)
            elif name=="rotate" and len(nums) in (1,3):
                angle=math.radians(nums[0]); c,s=math.cos(angle),math.sin(angle)
                rotation=(c,s,-s,c,0.,0.)
                if len(nums)==3:
                    px,py=nums[1:]
                    m=multiply(multiply((1.,0.,0.,1.,px,py),rotation),
                               (1.,0.,0.,1.,-px,-py))
                else:
                    m=rotation
            elif name=="matrix" and len(nums)==6:
                m=tuple(nums)
            else:
                raise ValueError("unsupported SVG transform "+name)
            result=multiply(result,m)
        if value[pos:].strip(" ,\\t\\r\\n"):
            raise ValueError("unparsed SVG transform")
        return result

    def attr(node, key, inherited=None):
        value=node.get(key)
        if value is not None:
            return value
        style=node.get("style","")
        m=re.search(r"(?:^|;)\\s*"+re.escape(key)+r"\\s*:\\s*([^;]+)",style)
        return m.group(1).strip() if m else inherited

    def coord(value, default=None):
        if value is None:return default
        m=re.fullmatch(r"\\s*([+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+))(?:px)?\\s*",value)
        return float(m.group(1)) if m else None

    outside,unverified,smallest=[],[],None
    identity=(1.,0.,0.,1.,0.,0.)
    def walk(node,matrix,inherited_size,inherited_anchor):
        nonlocal smallest
        tag=node.tag.rsplit("}",1)[-1]
        try:
            local=transforms(node.get("transform",""))
        except ValueError:
            unverified.append("unsupported transform")
            return
        matrix=multiply(matrix,local)
        size=coord(attr(node,"font-size"),inherited_size)
        anchor=attr(node,"text-anchor",inherited_anchor)
        if tag=="text":
            txt="".join(node.itertext()).strip()  # XML numeric entities decoded
            if not txt:return
            if len(list(node)) or not isinstance(size,(int,float)) or size<=0:
                unverified.append("complex or unknown text metrics")
                return
            if smallest is None or size<smallest[0]:
                smallest=(size,txt)
            x=coord(node.get("x"));y=coord(node.get("y"))
            if x is None or y is None:
                unverified.append("unresolved text coordinates")
                return
            # Font weight mostly changes stroke mass, not glyph advance width.
            # The original 0.58 bold-width multiplier overestimated a real
            # 600-weight title. All widths remain estimates, never approval.
            width=len(txt)*size*.52
            if anchor=="middle":low=x-width/2
            elif anchor=="end":low=x-width
            elif anchor in ("start",None,""):low=x
            else:
                unverified.append("unsupported text anchor")
                return
            # Conservative font-height estimate; not a real rendered glyph box.
            a,b,c,d,e,f=matrix
            points=[(low,y-size),(low+width,y-size),(low,y+size*.3),(low+width,y+size*.3)]
            transformed=[(a*px+c*py+e,b*px+d*py+f) for px,py in points]
            if not all(math.isfinite(v) for xy in transformed for v in xy):
                unverified.append("nonfinite text bounds")
                return
            xs=[p[0] for p in transformed];ys=[p[1] for p in transformed]
            if (min(xs)<vx-4 or max(xs)>vx+vw+4 or
                    min(ys)<vy-4 or max(ys)>vy+vh+4):
                outside.append(txt[:28])
            return
        for child in node:
            walk(child,matrix,size,anchor)
    walk(root,identity,coord(attr(root,"font-size"),16.),"start")
    result=[]
    if smallest and smallest[0]*scale<minimum_px-.05:
        required=minimum_px/scale
        result.append(
            f"the smallest label ({smallest[1][:24]!r}, {smallest[0]:g} units) "
            f"renders at {smallest[0]*scale:.1f} px on a 12.7-inch tablet, "
            f"under the {minimum_px:g} px floor: draw labels at least "
            f"{required:.0f} units high or adjust the viewBox")
    if outside:
        result.append("estimated transformed text bounds may extend outside the viewBox; "
                      "verify actual browser clipping: "+", ".join(repr(x) for x in outside[:3]))
    if unverified:
        result.append("SVG text geometry requires browser/author review: "+
                      ", ".join(sorted(set(unverified))))
    return result

'''


def patch_original_renderer(data: bytes) -> bytes:
    if hashlib.sha256(data).hexdigest() != ORIGINAL_RENDERER_SHA256:
        raise ValueError("ORIGINAL_SHARED_RENDERER_BYTE_PIN_MISMATCH")
    source = data.decode("utf8")
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("ORIGINAL_SHARED_CHECKER_ANCHOR_MISMATCH")
    begin=source.index(START)
    stop=source.index(END,begin)
    result=source[:begin]+REPLACEMENT+source[stop:]
    compile(result, "render_core.native_candidate.py", "exec")
    return result.encode("utf8")


def patch_to_private_file(source: Path, destination: Path) -> dict:
    source=Path(source).resolve();destination=Path(destination).resolve()
    if source==destination:
        raise ValueError("CANNOT_OVERWRITE_OWNER_SOURCE")
    # The original Shared tree must never be mutated by this candidate utility.
    if any(p.name=="Shared" for p in destination.parents):
        raise ValueError("OUTPUT_INSIDE_OWNER_SHARED_TREE_FORBIDDEN")
    data=source.read_bytes()
    candidate=patch_original_renderer(data)
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(candidate)
    return {
        "schema_version":"1.0.0","audit_type":"ORIGINAL_NATIVE_SHARED_SVG_CHECKER_PATCH_CANDIDATE",
        "original_sha256":hashlib.sha256(data).hexdigest(),
        "candidate_sha256":hashlib.sha256(candidate).hexdigest(),
        "original_source_unchanged":True,
        "native_render_rebuilt":False,
        "academic_status":"HOLD","native_shared_clearance":"NOT_PERFORMED",
        "release_status":"HOLD",
        "warning":"Candidate only. No original diagrams modified, no native author waivers, no academic approval.",
    }



# These original SVG bytes are Owner-local extracted textbook candidates, not
# canonical exam assets. Safe to store ONLY hashes/IDs in this public code.
ORIGINAL_INPUT_SOURCES_SHA256 = "ed0880d9ff314853c084834f2a8ac4ced69d2b8f5b019612ca999a1222b20565"
WPE_FIGURE_BYTES = {
    "REP-TB-FIG-06-INCLINE-BLOCK": (
        "work_energy_power_extracted/images/fig_06_incline_block.svg",
        "c5a896866e7fcca2b2dd82e8408394e655ab8b4ef8edda3a3eb6d80cbad6ccd5"),
    "REP-TB-FIG-07-INCLINE-FBD": (
        "work_energy_power_extracted/images/fig_07_incline_fbd.svg",
        "98c664df1595322694f974c7fde38699fc337a6f7829786b00e0dd5fd133e6bd"),
    "REP-TB-FIG-09-OVERHANGING-CHAIN": (
        "work_energy_power_extracted/images/fig_09_overhanging_chain.svg",
        "40510540074ad29b0f7634e680f8235356f64dbe969eb28b164edb7e30a00aa0"),
    "REP-TB-FIG-10-SPRING-BLOCK-WALL": (
        "work_energy_power_extracted/images/fig_10_spring_block_wall.svg",
        "c0a90c6fffcc88731316cb17fe34439e4bdccceda7a34d8deb585a2ba1d61bbc"),
}


def inspect_private_wpe_svg_sources(archive: Path, *, archive_pin: str = ORIGINAL_INPUT_SOURCES_SHA256,
                                    figure_pins: dict | None = None) -> dict:
    """Compare exact source SVG candidates using the proposed checker.

    This is *not* original native product re-render, figure approval, or a
    replacement for the pre-existing 10-gap authoritative render receipt.
    No figure text, image, authored solution or question content is returned.
    """
    import re
    import xml.etree.ElementTree as ET
    import zipfile
    pins = WPE_FIGURE_BYTES if figure_pins is None else figure_pins
    data_sha = hashlib.sha256()
    with Path(archive).open("rb") as reader:
        while chunk := reader.read(1048576):
            data_sha.update(chunk)
    if data_sha.hexdigest() != archive_pin:
        raise ValueError("OWNER_INPUT_SOURCES_ARCHIVE_HASH_MISMATCH")
    checker={}
    exec(REPLACEMENT, {"ET": ET, "re": re}, checker)
    check=checker["_figure_text_findings"]
    records=[]
    with zipfile.ZipFile(archive) as source:
        for figure_id,(member,byte_pin) in pins.items():
            info=source.getinfo(member)
            if info.is_dir() or not 0 < info.file_size <= 100000:
                raise ValueError("INVALID_OR_OVERSIZED_OWNER_SVG")
            original=source.read(member)
            if hashlib.sha256(original).hexdigest()!=byte_pin:
                raise ValueError("OWNER_SVG_BYTE_PIN_MISMATCH")
            try:
                findings=check(original.decode("utf8"),400.0,12.0)
            except UnicodeDecodeError as exc:
                raise ValueError("OWNER_SVG_ENCODING_INVALID") from exc
            records.append({
                "figure_id":figure_id,
                "source_sha256":byte_pin,
                "candidate_clipping_warnings":sum("outside the viewBox" in x for x in findings),
                "minimum_text_size_warnings":sum("smallest label" in x for x in findings),
                "unsupported_geometry_warnings":sum("requires browser/author review" in x for x in findings),
                "source_figure_modified":False,
                "owner_source_equivalence_to_printed_textbook": "NOT_CERTIFIED",
            })
    return {
        "schema_version":"1.0.0",
        "audit_type":"ORIGINAL_OWNER_TEXTBOOK_SVG_CHECKER_PATCH_CANDIDATE",
        "source_archive_sha256":data_sha.hexdigest(),
        "figure_results":records,
        "mechanical_status":"HOLD" if all(x["candidate_clipping_warnings"]==0 and x["unsupported_geometry_warnings"]==0 for x in records) else "FAIL",
        "original_native_receipt_gaps_waived":0,
        "uncreated_native_representations":6,
        "native_rebuild":"NOT_PERFORMED",
        "academic_status":"HOLD","release_status":"HOLD",
        "warning":"400px/12px source-level approximation is not the original manifest's exact tablet column, browser glyph metrics or a genuine new Shared render receipt.",
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description="Original Shared SVG checker candidate, Owner-local only")
    parser.add_argument("--original-renderer",required=True)
    parser.add_argument("--out",required=True)
    parser.add_argument("--receipt",required=True)
    parser.add_argument("--svg-archive",help="Optional exact Owner Input sources(4).zip; never copied")
    parser.add_argument("--svg-audit-out",help="Optional metadata-only four-source SVG comparison JSON")
    args=parser.parse_args(argv)
    originals=[Path(args.original_renderer).resolve(),Path(args.out).resolve(),Path(args.receipt).resolve()]
    if len(set(originals))!=3:
        raise ValueError("RECEIPT_SOURCE_AND_OUTPUT_MUST_BE_DISTINCT")
    result=patch_to_private_file(originals[0],originals[1])
    originals[2].parent.mkdir(parents=True,exist_ok=True)
    originals[2].write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    if bool(args.svg_archive) != bool(args.svg_audit_out):
        raise ValueError("SVG_SOURCE_AND_REPORT_MUST_BE_PAIRED")
    if args.svg_archive:
        svg_out=Path(args.svg_audit_out).resolve()
        if svg_out in set(originals)|{Path(args.svg_archive).resolve()}:
            raise ValueError("CANNOT_OVERWRITE_OWNER_INPUT_OR_RECEIPT")
        report=inspect_private_wpe_svg_sources(Path(args.svg_archive))
        svg_out.parent.mkdir(parents=True,exist_ok=True)
        svg_out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print("NATIVE_SHARED_SVG_CHECKER_CANDIDATE academic=HOLD release=HOLD")
    return 3


if __name__=="__main__":
    raise SystemExit(main())
