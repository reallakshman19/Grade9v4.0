"""Versioned, read-only evidence contracts for SL1/SL2 and downstream review.

PASS means the selected deterministic contract passed under the supplied local
trust pin. It does not establish document authenticity or academic correctness.
Standard library only. Vendored identically in both candidate skills.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "2.0.0-candidate"
SCHEMA = "smart-labelling-qrt-contract/v2"
GATES = ("integrity", "answer", "practice", "official_source", "official_key",
         "observations", "qrt", "canonical", "construction", "release")
OPERATIONS = {"RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}
FACTORS = ("concept_model_selection", "representation_translation", "reasoning_chain_length",
           "algebra_computational_load", "trap_exception_sensitivity")
HEX = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")


class Invalid(ValueError):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code, self.detail = code, str(detail)


def object_(value, where):
    if not isinstance(value, dict):
        raise Invalid("INVALID_TYPE", f"{where} must be an object")
    return value


def list_(value, where):
    if not isinstance(value, list):
        raise Invalid("INVALID_TYPE", f"{where} must be an array")
    return value


def text_(value, where):
    if not isinstance(value, str) or not value.strip():
        raise Invalid("MISSING_VALUE", f"{where} must be a nonempty string")
    return value


def unique(rows, key, where):
    result = {}
    for row in list_(rows, where):
        row = object_(row, where)
        identity = text_(row.get(key), f"{where}.{key}")
        if identity in result:
            raise Invalid("DUPLICATE_ID", f"{where}: duplicate {key} {identity}")
        result[identity] = row
    return result


def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise Invalid("DUPLICATE_JSON_KEY", key)
        obj[key] = value
    return obj


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(Invalid("INVALID_JSON", x)))
    except Invalid:
        raise
    except (OSError, UnicodeError, ValueError) as exc:
        raise Invalid("UNREADABLE_JSON", f"{path}: {exc}") from exc


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def file_digest(path):
    try:
        return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except OSError as exc:
        raise Invalid("ARTIFACT_MISSING", str(path)) from exc


def hash_(value, where):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise Invalid("INVALID_HASH", where)
    return value.removeprefix("sha256:")


def band(scores):
    scores = object_(scores, "scores")
    if set(scores) != set(FACTORS) or any(type(x) is not int or x not in (0, 1, 2) for x in scores.values()):
        raise Invalid("INVALID_DEMAND_VECTOR", "Exactly five integer scores, each 0..2, are required")
    total = sum(scores.values())
    return next(name for name, low, high in (("D1", 0, 2), ("D2", 3, 5), ("D3", 6, 7), ("D4", 8, 10)) if low <= total <= high)


def require(condition, code, detail):
    if not condition:
        raise Invalid(code, detail)


def pointer_value(data, pointer):
    pointer = text_(pointer, "JSON pointer")
    require(pointer.startswith("/"), "INVALID_POINTER", pointer)
    try:
        selected = data
        for segment in pointer[1:].split("/"):
            require(re.search(r"~(?![01])", segment) is None, "INVALID_POINTER", pointer)
            segment = segment.replace("~1", "/").replace("~0", "~")
            if isinstance(selected, list):
                require(re.fullmatch(r"0|[1-9][0-9]*", segment) is not None, "INVALID_POINTER", pointer)
                selected = selected[int(segment)]
            else:
                selected = selected[segment]
        return selected
    except Invalid:
        raise
    except (KeyError, ValueError, TypeError, IndexError) as exc:
        raise Invalid("POINTER_NOT_FOUND", pointer) from exc


def source_payloads(path, adapter, item_id):
    """Read a declared source shape without asserting its prior qualification."""
    require(isinstance(adapter, str) and adapter in {"examside-json/v1", "anchors-json/v1", "explicit-key-json/v1", "text-file/v1"}, "UNSUPPORTED_ADAPTER", str(adapter))
    if adapter == "text-file/v1":
        try:
            item = {"stem": Path(path).read_text(encoding="utf-8"), "options": None, "figs": []}
        except (OSError, UnicodeError) as exc:
            raise Invalid("UNREADABLE_TEXT", str(path)) from exc
    else:
        data = read_json(path)
        rows = data if isinstance(data, list) else object_(data, "source").get("items")
        items = unique(rows, "id", "source.items")
        item = items.get(item_id)
        require(item is not None, "SOURCE_ITEM_MISSING", str(item_id))
        item = dict(item)
        if adapter == "anchors-json/v1":
            require(not ({"figs", "figure_note", "stem", "key", "explanation", "type"} & set(item)),
                    "ADAPTER_SOURCE_SHAPE_MISMATCH", "Anchor aliases must not conceal conflicting source/figure fields")
            text_(item.get("text"), "anchor text")
            require(isinstance(item.get("options"), dict), "INVALID_TYPE", "anchor options must be an object")
            item.update(stem=item["text"], type=item.get("format"), figs=[])
            if "answer" in item:
                item["key"] = item["answer"]
            if "answer_basis" in item:
                item["explanation"] = item["answer_basis"]
        text_(item.get("stem"), "source stem")
        require("options" in item, "SOURCE_FIELD_MISSING", "options")
        if adapter != "anchors-json/v1":
            field = "figs" if adapter == "examside-json/v1" else "figure_note"
            require(field in item, "SOURCE_FIELD_MISSING", field)
            if adapter == "explicit-key-json/v1":
                require("figs" not in item, "ADAPTER_SOURCE_SHAPE_MISMATCH", "A source with actual figs must use the examside adapter")
            item["figs"] = item[field]
    payload = {"adapter": adapter, "item_id": item_id, "stem": item["stem"], "options": item["options"],
               "figs": item["figs"], "format": item.get("type")}
    return item, payload, {key: item[key] for key in ("key", "explanation") if key in item}


class Checker:
    def __init__(self, path, registry=None, registry_sha256=None):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.inputs, self.checks, self.artifacts = {}, [], {}
        self.reviewers_used = {}
        self.registry, self.registry_error = {}, None
        if registry is not None:
            try:
                actual = file_digest(registry)
                require(hash_(registry_sha256, "caller registry pin") == hash_(actual, "actual"),
                        "TRUST_PIN_MISMATCH", "The caller's registry pin does not match")
                reg = object_(read_json(registry), "review registry")
                require(reg.get("schema") == "smart-labelling-review-registry/v2", "REGISTRY_SCHEMA", "registry schema")
                self.registry = unique(reg.get("reviewers"), "id", "reviewers")
                self.artifacts[str(Path(registry).resolve())] = actual
            except Invalid as exc:
                self.registry_error = exc

    def resolve(self, value):
        value = Path(text_(value, "artifact.path"))
        return value.resolve() if value.is_absolute() else (self.root / value).resolve()

    def artifact(self, ref, locator=False):
        ref = object_(ref, "artifact ref")
        path = self.resolve(ref.get("path"))
        expected = hash_(ref.get("sha256"), f"{path} expected hash")
        actual = file_digest(path)
        self.artifacts[str(path)] = actual
        require(expected == hash_(actual, "actual"), "ARTIFACT_HASH_MISMATCH", str(path))
        if locator:
            text_(ref.get("locator"), "evidence locator")
        return path

    def evidence(self, refs):
        refs = list_(refs, "evidence_refs")
        require(bool(refs), "EVIDENCE_MISSING", "No evidence references")
        for ref in refs:
            self.artifact(ref, locator=True)

    def review(self, ref, role, subject, author):
        if self.registry_error:
            raise self.registry_error
        require(bool(self.registry), "TRUST_REGISTRY_REQUIRED", "Supply the Owner-trusted registry and its independent CLI hash pin")
        review = object_(read_json(self.artifact(ref)), "review")
        require(review.get("schema") == "smart-labelling-review/v2", "REVIEW_SCHEMA", role)
        require(review.get("role") == role and review.get("status") == "APPROVED", "REVIEW_NOT_APPROVED", role)
        reviewer = text_(review.get("reviewer"), "reviewer")
        require(reviewer != author and review.get("author") == author, "REVIEW_NOT_INDEPENDENT", role)
        actor = self.registry.get(reviewer, {})
        require(actor.get("status") == "ACTIVE" and role in list_(actor.get("roles", []), "reviewer.roles"),
                "REVIEWER_NOT_AUTHORIZED", f"{reviewer}: {role}")
        require(review.get("subject_digest") == digest(subject), "REVIEW_SUBJECT_CHANGED", role)
        text_(review.get("findings"), "review.findings")
        self.evidence(review.get("evidence_refs"))
        self.reviewers_used[(role, digest(subject))] = reviewer
        return object_(review.get("decision"), "review.decision")

    def source(self, spec):
        spec = object_(spec, "source")
        path = self.artifact(spec)
        adapter = spec.get("adapter")
        item, payload, answer_payload = source_payloads(path, adapter, spec.get("item_id"))
        require(spec.get("question_digest") == digest(payload), "QUESTION_CHANGED", "Question/format/figure references changed")
        require(spec.get("answer_digest") == digest(answer_payload), "ANSWER_SOURCE_CHANGED", "Key/explanation changed")
        refs = []

        def figure_refs(value):
            if isinstance(value, str) and value:
                refs.append(value)
            elif isinstance(value, list):
                for entry in value:
                    figure_refs(entry)
            elif isinstance(value, dict):
                for entry in value.values():
                    figure_refs(entry)
            elif value is not None:
                raise Invalid("INVALID_FIGURES", "figs must contain strings, arrays or objects")

        # Legacy figure_note is descriptive text; only examside figs are asset locators.
        if adapter == "examside-json/v1":
            figure_refs(item["figs"])
        assets = unique(spec.get("figure_assets", []), "source_ref", "figure_assets")
        require(set(refs) == set(assets), "FIGURE_ASSET_BINDING", "Every actual figure reference needs its saved asset and hash")
        for asset in assets.values():
            self.artifact(asset)
        return item, payload

    def span(self, span):
        span = object_(span, "passage span")
        path = self.artifact(span.get("artifact"))
        try:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        except (OSError, UnicodeError) as exc:
            raise Invalid("PASSAGE_UNREADABLE", str(path)) from exc
        start, end = span.get("start_line"), span.get("end_line")
        require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                "PASSAGE_RANGE", str(path))
        selected = "".join(lines[start-1:end])
        actual = "sha256:" + hashlib.sha256(selected.encode("utf-8")).hexdigest()
        require(hash_(span.get("text_sha256"), "passage hash") == hash_(actual, "actual"),
                "PASSAGE_CHANGED", str(path))

    def run_gate(self, record, gate, action):
        try:
            value = action()
            record["gates"][gate] = "PASS" if value is not False else "NOT_APPLICABLE"
            self.checks.append({"question_id": record["question_id"], "gate": gate, "status": record["gates"][gate]})
            return value
        except Invalid as exc:
            record["gates"][gate] = "HOLD"
            record["issues"].append({"gate": gate, "code": exc.code, "detail": exc.detail})
            self.checks.append({"question_id": record["question_id"], "gate": gate, "status": "HOLD"})
            return None

    def answer(self, spec, source, source_spec, sl1):
        spec = object_(spec, "answer_reference")
        kind = spec.get("kind")
        labelled = sl1["content_integrity"]["answer_check"].get("key")
        if kind == "NO_KEY":
            require(labelled in (None, ""), "UNSUPPORTED_COPIED_KEY", "A copied key has no resolved reference")
            return False
        if kind == "PUBLISHER_FIELD":
            require("key" in source and source["key"] not in (None, ""), "ANSWER_FIELD_UNSUPPORTED", "Adapter found no explicit publisher key")
            value = source["key"]
        elif kind == "REVIEWED_EXTRACTION":
            extraction = object_(read_json(self.artifact(spec.get("artifact"))), "answer extraction")
            require(extraction.get("schema") == "smart-labelling-answer-extraction/v2", "EXTRACTION_SCHEMA", "answer extraction")
            require(extraction.get("source_item_id") == source_spec.get("item_id") and
                    extraction.get("source_answer_digest") == source_spec.get("answer_digest"),
                    "EXTRACTION_STALE", "Extraction is not bound to the current source answer text")
            value = extraction.get("answer")
            decision = self.review(spec.get("review_ref"), "answer_extraction", extraction, text_(extraction.get("author"), "extraction.author"))
            require(decision.get("answer") == value, "EXTRACTION_REVIEW_MISMATCH", "Reviewed answer differs")
        else:
            raise Invalid("ANSWER_REFERENCE_UNSUPPORTED", str(kind))
        require(value not in (None, "") and value == spec.get("value") == labelled,
                "SOURCE_KEY_CHANGED", "Current answer reference and copied SL1 key disagree")
        return value

    def observation(self, spec, sl1, sl2, question_digest, answer_digest, author, answer_resolved):
        learner = object_(sl2.get("learner"), "learner")
        if sl2.get("mode") == "QUESTION":
            require(spec is None, "QUESTION_HAS_OBSERVATION", "QUESTION mode must not attach a learner observation")
            return False
        require(sl2.get("mode") == "EVIDENCE", "INVALID_MODE", str(sl2.get("mode")))
        spec = object_(spec, "observation")
        data = object_(read_json(self.artifact(spec.get("attempts_ref"))), "attempt file")
        attempts = unique(data.get("attempts"), "attempt_id", "attempts")
        attempt = attempts.get(learner.get("attempt_ref"))
        require(attempt is not None and spec.get("attempt_id") == learner.get("attempt_ref"), "ATTEMPT_NOT_FOUND", "Saved attempt ID")
        require(spec.get("snapshot_digest") == digest(attempt), "ATTEMPT_SNAPSHOT_CHANGED", "Saved observation changed")
        require(attempt.get("question_id") == sl1["question_id"] and
                attempt.get("item_digest") == sl1["custody"].get("item_digest") and
                attempt.get("question_version") == sl1.get("version") and
                attempt.get("question_digest") == question_digest,
                "ATTEMPT_BINDING_MISMATCH", "Question identity, version or full payload differs")
        require(attempt.get("stage") == spec.get("stage") == "P1", "OBSERVATION_STAGE_UNSUPPORTED", "Only actual pre-teaching P1 observations are supported here")
        require(attempt.get("task_id") == spec.get("task_id") == sl1["question_id"], "ATTEMPT_TASK_MISMATCH", "A different bound task cannot inherit this source observation")
        for target, source in (("original_answer", "answer"), ("reasoning", "reasoning"), ("confidence", "confidence"),
                               ("committed_before_feedback", "committed_before_feedback")):
            require(source in attempt and target in learner and learner[target] == attempt[source],
                    "ATTEMPT_FIELD_MISMATCH", target)
        require(attempt.get("saved") is True, "ATTEMPT_NOT_SAVED", "Commit alone does not prove successful persistence")
        seq = attempt.get("save_sequence")
        feedback = attempt.get("feedback_sequence")
        require(type(seq) is int and seq >= 0 and "feedback_sequence" in attempt and
                (feedback is None or type(feedback) is int and feedback >= 0),
                "SAVE_ORDER_UNKNOWN", "Explicit save and feedback order is required")
        committed = feedback is None or seq < feedback
        require(attempt.get("committed_before_feedback") is committed, "SAVE_ORDER_CONTRADICTION", "Commit flag disagrees with event order")
        earlier = [a for a in attempts.values() if a.get("task_id") == attempt["task_id"] and
                   a.get("question_digest") == question_digest and a.get("question_version") == attempt["question_version"] and
                   a.get("stage") == "P1" and a.get("saved") is True]
        require(all(type(a.get("save_sequence")) is int for a in earlier), "SAVE_ORDER_UNKNOWN", "Other saved attempts have unknown order")
        require(sum(a["save_sequence"] == seq for a in earlier) == 1 and min(a["save_sequence"] for a in earlier) == seq,
                "NOT_FIRST_SAVED_ATTEMPT", "Select the unique earliest saved attempt for this task/version/stage")
        help_value = attempt.get("help_before_commit", "UNKNOWN")
        require(help_value is not None and type(help_value) is str and help_value != "", "HELP_HISTORY_UNKNOWN", "Missing/false help is not independent")
        expected_help = "INDEPENDENT" if help_value in ("NONE", "INDEPENDENT") else help_value
        require(expected_help in {"INDEPENDENT", "HINT", "SCAFFOLD", "EXPLANATION", "WORKED_EXAMPLE", "FULL_SOLUTION", "UNKNOWN"},
                "INVALID_HELP_HISTORY", str(help_value))
        require(learner.get("help_exposure") == expected_help, "HELP_EXPOSURE_MISMATCH", "Saved exposure differs from the copied learner field")
        exposures = attempt.get("exposures_before_save")
        if expected_help == "INDEPENDENT":
            require(committed and exposures == [], "FALSE_INDEPENDENT_ATTEMPT", "Independence requires saved work before feedback and an explicitly empty exposure history")
        elif expected_help != "UNKNOWN":
            require(isinstance(exposures, list) and expected_help in exposures, "EXPOSURE_HISTORY_MISMATCH", "Assistance is not recorded in the exposure history")
        else:
            require(learner.get("result") == "NOT_EVALUATED" and
                    all(x == "UNKNOWN" for x in object_(learner.get("prerequisite_state"), "prerequisite_state").values()),
                    "UNKNOWN_HELP_CANNOT_SUPPORT_INFERENCE", "Preserve the observation without an independence or capability claim")
        interpretation = {k: learner.get(k) for k in ("result", "prerequisite_state", "failure_hypothesis")}
        has_inference = (interpretation["result"] != "NOT_EVALUATED" or interpretation["failure_hypothesis"] is not None or
                         any(x != "UNKNOWN" for x in object_(interpretation["prerequisite_state"], "prerequisite_state").values()))
        if has_inference:
            require(answer_resolved, "INTERPRETATION_ANSWER_UNRESOLVED", "Interpretation requires a current resolved answer reference")
            subject = {"attempt_digest": digest(attempt), "answer_digest": answer_digest, "interpretation": interpretation}
            decision = self.review(spec.get("interpretation_review_ref"), "learner_interpretation", subject, author)
            require(decision.get("interpretation") == interpretation, "INTERPRETATION_REVIEW_MISMATCH", "Derived learner claims differ")
        return {"attempt_id": attempt["attempt_id"], "raw_observation_digest": digest(attempt),
                "help": expected_help, "independence": "UNKNOWN" if expected_help == "UNKNOWN" else
                ("INDEPENDENT" if expected_help == "INDEPENDENT" else "ASSISTED"), "interpretation_reviewed": has_inference}

    def cognitive_seed(self, seed, sl2, source):
        seed = object_(seed, "cognitive_seed")
        require(seed.get("schema") == "smart-labelling-cognitive-seed/v2", "SEED_SCHEMA", "cognitive seed")
        roles = unique(seed.get("decisive_roles"), "id", "decisive_roles")
        require(bool(roles), "DECISIVE_ROLE_MISSING", "One or more decisive roles are needed")
        moves = unique(sl2["route"].get("moves"), "id", "route.moves")
        for role in roles.values():
            text_(role.get("intellectual_work"), "role.intellectual_work")
            refs = list_(role.get("route_move_refs"), "route_move_refs")
            require(bool(refs) and all(isinstance(x, str) and x in moves for x in refs), "ROUTE_REF_MISSING", "Decisive role references an absent route move")
        for field in ("inputs", "outputs", "conditions", "dependencies", "boundary_checks", "wrong_move_hypotheses", "competing_operations"):
            values = list_(seed.get(field), f"seed.{field}")
            require(bool(values), "SEED_FIELD_EMPTY", field)
            for value in values:
                object_(value, field)
        for role in seed["inputs"] + seed["outputs"]:
            text_(role.get("role"), "input/output role")
            pointer_value(source, role.get("source_pointer"))
        for condition in seed["conditions"]:
            text_(condition.get("condition"), "seed.condition")
        for dependency in seed["dependencies"]:
            text_(dependency.get("role"), "seed.dependency.role")
            require(dependency.get("authority_status") in {"REQUIRED", "UNQUALIFIED", "NOT_APPLICABLE"},
                    "SEED_AUTHORITY_OWNERSHIP", "SL2 records an authority requirement; qualification belongs to the binder")
        for check in seed["boundary_checks"]:
            require(check.get("route_ref") in moves, "ROUTE_REF_MISSING", "boundary route")
            text_(check.get("check"), "seed.boundary_check")
        hypotheses = list_(sl2.get("wrong_route_hypotheses"), "wrong_route_hypotheses")
        for hypothesis in seed["wrong_move_hypotheses"]:
            index = hypothesis.get("hypothesis_ref")
            require(hypothesis.get("status") == "HYPOTHESIS" and type(index) is int and 0 <= index < len(hypotheses),
                    "HYPOTHESIS_REF_MISSING", "Link the proposed wrong move to its existing SL2 hypothesis")
            require(hypothesis.get("route_ref") in moves, "ROUTE_REF_MISSING", "wrong-move route")
        for alternative in seed["competing_operations"]:
            require(alternative.get("operation") in OPERATIONS and alternative.get("operation") != sl2["demand_proposal"]["primary"],
                    "INVALID_COMPETING_OPERATION", "Use a different existing operation ID")
            text_(alternative.get("reason"), "competing reason")
        operation = sl2["demand_proposal"]["primary"]
        structure = object_(seed.get("operation_structure"), "operation_structure")
        fields = {"EXPLAIN": ("mechanism",), "APPLY": ("rule", "conditions"),
                  "MODEL": ("variables", "assumptions"), "REPRESENT": ("correspondences", "invariants"),
                  "SYNTHESIZE": ("dependency_roles", "traversal"), "JUSTIFY": ("claim", "warrant", "scope")}
        if operation == "RETRIEVE":
            require(structure.get("kind") in ("RECALL", "CLASSIFY"), "RETRIEVE_KIND", "Recall or classify")
            required = ("cue", "target") if structure["kind"] == "RECALL" else ("criteria", "exclusions")
        else:
            require(operation in fields, "INVALID_OPERATION", str(operation))
            required = fields[operation]
        for field in required:
            require(bool(structure.get(field)), "OPERATION_STRUCTURE_MISSING", field)
        assessment = object_(seed.get("independent_demand"), "independent_demand")
        text_(assessment.get("assessor"), "assessor")
        require(assessment.get("basis") == "TASK_INTRINSIC" and assessment.get("prior_score_seen") is False,
                "INDEPENDENT_DEMAND_NOT_ESTABLISHED", "Declare a task-intrinsic first assessment before comparison")
        require(assessment.get("operation") == operation, "DEMAND_OPERATION_MISMATCH", operation)
        scores = assessment.get("scores")
        band(scores)
        current = {k: sl2["difficulty_evidence"]["components"][k]["score"] for k in FACTORS}
        require(scores == current, "DEMAND_VECTOR_MISMATCH", "Every factor must match, not only the total")
        refs = object_(assessment.get("factor_route_refs"), "factor_route_refs")
        for factor in FACTORS:
            ids = list_(refs.get(factor), factor)
            require(bool(ids) and all(isinstance(x, str) and x in moves for x in ids), "FACTOR_EVIDENCE_MISSING", factor)
        comparison = assessment.get("prior_comparison")
        actual_prior = sl2["difficulty_evidence"].get("prior_proposal")
        if actual_prior is not None:
            actual_prior = object_(actual_prior, "prior_proposal")
            require(comparison is not None, "PRIOR_COMPARISON_MISSING", "The existing prior proposal must remain visible")
            comparison = object_(comparison, "prior_comparison")
            require(comparison.get("proposal_digest") == digest(actual_prior), "PRIOR_PROPOSAL_CHANGED", "Compare the exact saved prior proposal")
            raw_scores = actual_prior.get("scores")
            if isinstance(raw_scores, str):
                try:
                    raw_scores = [int(x) for x in raw_scores.split("/")]
                except ValueError as exc:
                    raise Invalid("PRIOR_VECTOR_UNSUPPORTED", "Could not resolve the prior factor vector") from exc
            if isinstance(raw_scores, list) and len(raw_scores) == 5:
                raw_scores = dict(zip(FACTORS, raw_scores))
            band(raw_scores)
            require(raw_scores == comparison.get("scores"), "PRIOR_VECTOR_MISMATCH", "The saved prior factors differ from the comparison")
        if comparison is not None:
            comparison = object_(comparison, "prior_comparison")
            prior = comparison.get("scores")
            band(prior)
            if prior != scores:
                text_(comparison.get("differences"), "factor disagreement, including equal-total disagreements")
                require(comparison["differences"].strip().lower() not in {"none", "unchanged", "no difference"},
                        "DISAGREEMENT_SUPPRESSED", "Changed factors need an actual disagreement record")
        return {"operation": operation, "scores": scores, "band": band(scores), "seed_digest": digest(seed)}

    def construction(self, spec, qrt, qrt_subject, canonical):
        spec = object_(spec, "construction")
        require(qrt is not None and canonical is not None, "CONSTRUCTION_DEPENDENCIES", "Reviewed QRT and qualified warrants are required")
        author = text_(spec.get("author"), "construction.author")
        self.evidence(spec.get("blueprint_refs"))
        self.artifact(spec.get("topic_adapter_ref"))
        task_id = text_(spec.get("task_id"), "bound task id")
        require(task_id != qrt_subject["question_id"], "BOUND_TASK_IDENTITY_CONFLATED", "An authored task needs a distinct identity")
        require(spec.get("source_question_id") == qrt_subject["question_id"] and spec.get("source_role") == qrt["source_role"],
                "BOUND_SOURCE_RELATIONSHIP_MISMATCH", "Preserve the reviewed source identity and relationship")
        text_(spec.get("family_id"), "family id")
        teacher, learner = object_(spec.get("core1a"), "core1a"), object_(spec.get("core1b"), "core1b")
        text_(teacher.get("task_id"), "Core1A task id")
        text_(learner.get("task_id"), "Core1B task id")
        require(teacher.get("task_id") != qrt_subject["question_id"] and teacher.get("source_kind") == "AUTHORED_NON_EXAM",
                "TEACHER_SOURCE_NOT_DISTINCT", "Core1A needs its own different non-exam worked construction, with origin reviewed under B1-B7")
        require(teacher.get("task_id") != learner.get("task_id") and learner.get("task_id") == task_id,
                "CONSTRUCTION_NOT_FRESH", "Teacher and learner tasks must be distinct")
        teacher_path, learner_path = self.artifact(teacher["artifact"]), self.artifact(learner["artifact"])
        require(file_digest(teacher_path) != file_digest(learner_path), "CONSTRUCTION_NOT_FRESH", "Identical teaching and assessment artifacts")
        roles = unique(spec.get("roles"), "id", "construction.roles")
        require(bool(roles), "BRIDGE_ROLES_MISSING", "No teaching/reconstruction correspondence")
        for role in roles.values():
            teaching = list_(role.get("teaching_spans"), "teaching_spans")
            reconstruction = list_(role.get("reconstruction_spans"), "reconstruction_spans")
            purpose = role.get("assessment_role")
            require(purpose in {"TARGET", "PREREQUISITE", "SUPPORT"}, "BRIDGE_ROLE_UNDECLARED", role["id"])
            require(type(role.get("required_by_core1b")) is bool, "BRIDGE_ROLE_UNDECLARED", "required_by_core1b")
            if role["required_by_core1b"] or purpose == "TARGET":
                require(bool(teaching) and bool(reconstruction), "BRIDGE_ROLE_NOT_TAUGHT_OR_ELICITED", role["id"])
            for span in teaching:
                self.span(span)
                require(self.resolve(span["artifact"]["path"]) == teacher_path, "BRIDGE_WRONG_PASSAGE_OWNER", "Core1A role span")
            for span in reconstruction:
                self.span(span)
                require(self.resolve(span["artifact"]["path"]) == learner_path, "BRIDGE_WRONG_PASSAGE_OWNER", "Core1B role span")
        criteria = object_(spec.get("bridge_evidence"), "bridge_evidence")
        require(set(criteria) == {f"B{i}" for i in range(1, 8)}, "BRIDGE_WITNESS_INCOMPLETE", "B1 through B7 required")
        for refs in criteria.values():
            refs = list_(refs, "bridge criterion spans")
            require(bool(refs), "BRIDGE_CRITERION_EVIDENCE_MISSING", "Each B1-B7 criterion needs actual passage/evidence spans")
            for span in refs:
                self.span(span)
        subject = {"construction": {k: v for k, v in spec.items() if k not in {"review_ref", "runtime_review_ref", "acceptance_review_ref"}},
                   "qrt_subject": qrt_subject, "qrt_decision": qrt, "canonical": canonical}
        decision = self.review(spec.get("review_ref"), "construction", subject, author)
        require(decision.get("criteria") == {f"B{i}": True for i in range(1, 8)} and
                decision.get("teaching_sufficient") is True and decision.get("fresh_reconstruction") is True,
                "BRIDGE_SEMANTICS_NOT_QUALIFIED", "Independent B1-B7 qualification is incomplete")
        scores = decision.get("scores")
        target_band = band(scores)
        require(decision.get("operation") == qrt["target"]["operation"] and target_band == qrt["target"]["band"],
                "BOUND_TARGET_DEMAND_MISMATCH", "Bound task needs its own matching operation/demand")
        return subject, decision

    def canonical(self, spec):
        spec = object_(spec, "canonical")
        warrants = unique(spec.get("warrants"), "id", "canonical.warrants")
        require(bool(warrants), "CANONICAL_NOT_QUALIFIED", "No qualified warrants are bound")
        result = []
        for warrant in warrants.values():
            data = read_json(self.artifact(warrant.get("artifact")))
            pointer = text_(warrant.get("pointer"), "warrant JSON pointer")
            selected = pointer_value(data, pointer)
            subject = {"id": warrant["id"], "pointer": pointer, "warrant_digest": digest(selected),
                       "authority_version": warrant.get("authority_version")}
            text_(subject["authority_version"], "authority_version")
            decision = self.review(warrant.get("review_ref"), "canonical", subject, text_(warrant.get("author"), "warrant author"))
            require(decision.get("qualified") is True and bool(decision.get("conditions")), "WARRANT_UNQUALIFIED", warrant["id"])
            result.append({**subject, "qualification": decision, "review_ref": warrant["review_ref"]})
        return result

    def record(self, entry, sl1, sl2, allow_partial_practice):
        qid = sl1["question_id"]
        result = {"question_id": qid, "gates": {gate: "NOT_RUN" for gate in GATES}, "issues": [],
                  "derived_state": "CURRENT", "observed": None, "qrt_decision": None}
        author1 = self.inputs["sl1"].get("labeller")
        author2 = self.inputs.get("sl2", {}).get("labeller")
        source_spec = entry.get("source")
        source = None

        def integrity():
            nonlocal source
            require(entry.get("sl1_record_digest") == digest(sl1), "SL1_RECORD_CHANGED", qid)
            if sl2 is not None:
                require(entry.get("sl2_record_digest") == digest(sl2), "SL2_RECORD_CHANGED", qid)
            require(sl1.get("status") != "STALE" and (sl2 is None or sl2.get("status") != "STALE"), "STALE_RECORD", qid)
            source, _ = self.source(source_spec)
            custody = object_(sl1.get("custody"), "SL1 custody")
            source_path = self.resolve(source_spec["path"])
            legacy_path = custody.get("text_file") if source_spec["adapter"] == "text-file/v1" else custody.get("source_file")
            require(source_path == self.resolve(legacy_path), "SOURCE_PATH_MISMATCH", qid)
            if source_spec["adapter"] != "text-file/v1":
                require(source_spec.get("item_id") == custody.get("source_item_id"), "SOURCE_ID_MISMATCH", qid)
                if "paper" in source:
                    require(source.get("paper") == sl1["source_identity"].get("paper"), "SOURCE_PAPER_MISMATCH", qid)
            key_field = "answer" if source_spec["adapter"] == "anchors-json/v1" else "key"
            require(not custody.get("source_key_field") or custody["source_key_field"] == key_field, "UNDECLARED_KEY_LOCATOR", "Use the adapter's fixed key locator")
            if sl1.get("format", {}).get("figure") == "ESSENTIAL":
                require(bool(source_spec.get("figure_assets")), "ESSENTIAL_FIGURE_NOT_BOUND", "A validated description is not a bound figure asset")
            for label, record, author in (("sl1", sl1, author1), ("sl2", sl2, author2)):
                if record is not None and record.get("status") == "REVIEWED":
                    self.review(entry.get(label + "_review_ref"), label, {"record_digest": digest(record),
                                "question_digest": source_spec["question_digest"], "answer_digest": source_spec["answer_digest"],
                                "library_sha256": self.contract["inputs"]["library"]["sha256"],
                                "vocabulary_sha256": self.contract["inputs"]["vocabulary"]["sha256"]}, author)
            return True

        self.run_gate(result, "integrity", integrity)
        if source is None or result["gates"]["integrity"] != "PASS":
            result["derived_state"] = "STALE_OR_UNRESOLVED"
            return result
        source_subject = {"question_id": qid, "question_digest": source_spec["question_digest"],
                          "identity": sl1["source_identity"]}

        def official_source():
            spec = object_(entry.get("official_source"), "official_source")
            self.evidence(spec.get("evidence_refs"))
            subject = {**source_subject, "evidence_refs": spec["evidence_refs"]}
            decision = self.review(spec.get("review_ref"), "source_custody", subject, author1)
            require(decision.get("source_item_id") == source_spec.get("item_id") and
                    decision.get("paper") == sl1["source_identity"].get("paper") and
                    decision.get("question_digest") == source_spec["question_digest"],
                    "OFFICIAL_QUESTION_MAPPING_MISMATCH", qid)
            text_(decision.get("official_item_locator"), "official question locator")
            return decision

        self.run_gate(result, "official_source", official_source)
        answer_value = self.run_gate(result, "answer", lambda: self.answer(entry.get("answer_reference"), source, source_spec, sl1))
        answer_binding_digest = digest({"source_answer_digest": source_spec["answer_digest"],
                                        "answer_reference": entry.get("answer_reference"),
                                        "sl1_answer_check": sl1["content_integrity"]["answer_check"]})

        def official_key():
            require(result["gates"]["answer"] == "PASS", "ANSWER_UNRESOLVED", qid)
            spec = object_(entry.get("official_key"), "official_key")
            self.evidence(spec.get("evidence_refs"))
            subject = {**source_subject, "source_answer_digest": source_spec["answer_digest"],
                       "answer": answer_value, "evidence_refs": spec["evidence_refs"]}
            decision = self.review(spec.get("review_ref"), "key_custody", subject, author1)
            require(decision.get("answer") == answer_value and decision.get("source_item_id") == source_spec.get("item_id"),
                    "OFFICIAL_KEY_MAPPING_MISMATCH", qid)
            mapping = object_(decision.get("option_mapping"), "option_mapping")
            require(mapping.get("source_options_digest") == digest(source.get("options")) and mapping.get("source_answer") == answer_value,
                    "KEY_OPTION_MAPPING_MISMATCH", qid)
            if mapping.get("kind") == "MCQ":
                choices = object_(mapping.get("official_to_source"), "official_to_source")
                official_answer = mapping.get("official_answer")
                require(isinstance(official_answer, str) and official_answer in choices and choices[official_answer] == answer_value,
                        "KEY_OPTION_MAPPING_MISMATCH", qid)
            else:
                require(mapping.get("kind") in {"NUMERICAL", "TEXT"} and "official_answer" in mapping,
                        "KEY_OPTION_MAPPING_MISSING", qid)
            text_(decision.get("official_key_locator"), "official key row locator")
            return decision

        self.run_gate(result, "official_key", official_key)
        # Unsupported claims invalidate the claim; honest PARTIAL analysis is unaffected.
        if sl1["source_verification"].get("status") == "VERIFIED" and result["gates"]["official_source"] != "PASS":
            result["gates"]["integrity"] = "HOLD"
            result["issues"].append({"gate": "integrity", "code": "UNSUPPORTED_VERIFIED_SOURCE", "detail": qid})
        if sl2 is not None and sl2["binding"].get("answer_ref_status") == "KEY_VERIFIED" and result["gates"]["official_key"] != "PASS":
            result["gates"]["integrity"] = "HOLD"
            result["issues"].append({"gate": "integrity", "code": "UNSUPPORTED_VERIFIED_KEY", "detail": qid})

        def practice():
            require(result["gates"]["integrity"] == "PASS", "INTEGRITY_HOLD", qid)
            require(result["gates"]["answer"] == "PASS", "ANSWER_UNRESOLVED", qid)
            require(sl1["workflow_action"].get("value") == "READY_FOR_FIRST_TRY", "NOT_READY_FOR_FIRST_TRY", qid)
            if result["gates"]["official_source"] != "PASS":
                require(allow_partial_practice and sl1["source_verification"].get("status") != "VERIFIED", "PARTIAL_PRACTICE_POLICY_REQUIRED", qid)
            return True

        self.run_gate(result, "practice", practice)
        if sl2 is not None:
            result["observed"] = self.run_gate(result, "observations", lambda: self.observation(entry.get("observation"), sl1, sl2,
                           source_spec["question_digest"], answer_binding_digest, author2, result["gates"]["answer"] == "PASS"))
            qrt_subject = {"question_id": qid, "question_digest": source_spec["question_digest"],
                           "answer_digest": source_spec["answer_digest"], "sl1_record_digest": digest(sl1),
                           "sl2_record_digest": digest(sl2), "seed": entry.get("cognitive_seed"),
                           "library_semantic_digest": digest(self.inputs["library"]),
                           "rubric_sha256": self.contract["inputs"]["vocabulary"]["sha256"]}

            def qrt():
                require(result["gates"]["integrity"] == "PASS", "INTEGRITY_HOLD", qid)
                proposal = self.cognitive_seed(entry.get("cognitive_seed"), sl2, source)
                decision = self.review(entry.get("qrt_review_ref"), "qrt", qrt_subject, author2)
                require(decision.get("operation") in OPERATIONS and decision.get("independently_scored") is True,
                        "QRT_INDEPENDENT_ASSESSMENT_MISSING", qid)
                first = object_(read_json(self.artifact(decision.get("first_assessment_ref"))), "independent first assessment")
                require(first.get("schema") == "smart-labelling-independent-demand/v2" and first.get("question_id") == qid and
                        first.get("question_digest") == source_spec["question_digest"] and
                        first.get("rubric_sha256") == self.contract["inputs"]["vocabulary"]["sha256"],
                        "FIRST_ASSESSMENT_BINDING", qid)
                require(first.get("assessor") == self.reviewers_used[("qrt", digest(qrt_subject))] and
                        first.get("prior_score_seen") is False and first.get("operation") in OPERATIONS,
                        "FIRST_ASSESSMENT_NOT_INDEPENDENT", qid)
                band(first.get("scores"))
                evidence = object_(first.get("factor_evidence"), "first assessment factor evidence")
                for factor in FACTORS:
                    text_(evidence.get(factor), "first assessment evidence: " + factor)
                before, after = first.get("saved_sequence"), decision.get("comparison_sequence")
                require(type(before) is int and type(after) is int and 0 <= before < after,
                        "FIRST_ASSESSMENT_ORDER_UNKNOWN", qid)
                resolved_band = band(decision.get("scores"))
                if decision["scores"] != proposal["scores"] or decision["operation"] != proposal["operation"] or first["scores"] != decision["scores"] or first["operation"] != decision["operation"]:
                    text_(decision.get("differences"), "QRT factor/operation disagreement")
                role = decision.get("source_role")
                require(role in {"DIRECT_EXAM_EVIDENCE", "PREREQUISITE_BRIDGE", "AUTHORED_TRANSFER"}, "SOURCE_ROLE_UNRESOLVED", qid)
                target = object_(decision.get("target"), "QRT target")
                require(target.get("operation") in OPERATIONS and target.get("band") in {"D1", "D2", "D3", "D4"}, "INVALID_QRT_TARGET", qid)
                if role == "DIRECT_EXAM_EVIDENCE":
                    require(decision["operation"] == target["operation"] and resolved_band == target["band"], "DIRECT_SOURCE_TARGET_MISMATCH", qid)
                    require(result["gates"]["official_source"] == result["gates"]["official_key"] == "PASS", "EXAM_CUSTODY_HOLD", qid)
                if role == "AUTHORED_TRANSFER":
                    require(sl1["source_identity"].get("authority") == "AUTHORED", "AUTHORED_SOURCE_IDENTITY_REQUIRED", qid)
                home = text_(decision.get("primary_home"), "primary_home")
                secondary = list_(decision.get("secondary_homes"), "secondary_homes")
                require(all(isinstance(x, str) and x != home for x in secondary) and len(set(secondary)) == len(secondary),
                        "DUPLICATE_COVERAGE_HOME", qid)
                return decision

            qrt_decision = self.run_gate(result, "qrt", qrt)
            result["qrt_decision"] = qrt_decision
        else:
            qrt_subject, qrt_decision = None, None
        canonical = self.run_gate(result, "canonical", lambda: self.canonical(entry.get("canonical")))
        bound = self.run_gate(result, "construction", lambda: self.construction(entry.get("construction"), qrt_decision, qrt_subject, canonical))

        def release():
            require(bound is not None, "CONSTRUCTION_HOLD", qid)
            spec = entry["construction"]
            runtime = object_(spec.get("runtime"), "construction.runtime")
            self.evidence(runtime.get("compiled_artifacts"))
            self.evidence(runtime.get("baseline_artifacts"))
            subject = {"bound_subject_digest": digest(bound[0]), "bound_decision": bound[1], "runtime": runtime}
            decision = self.review(spec.get("runtime_review_ref"), "runtime", subject, spec["author"])
            require(all(decision.get(k) is True for k in ("protected_work", "save_before_feedback", "content_preserved")),
                    "RUNTIME_NOT_QUALIFIED", qid)
            accepted = self.review(spec.get("acceptance_review_ref"), "acceptance", subject, spec["author"])
            require(accepted.get("learner_acceptance") is True, "LEARNER_ACCEPTANCE_OPEN", qid)
            return True

        self.run_gate(result, "release", release)
        result["dependency_trace"] = {"source_question": source_spec["question_digest"], "source_answer": source_spec["answer_digest"],
                                      "sl1": digest(sl1), "sl2": digest(sl2) if sl2 else None,
                                      "seed": digest(entry["cognitive_seed"]) if entry.get("cognitive_seed") else None,
                                      "qrt_review": entry.get("qrt_review_ref"),
                                      "bound_task_id": (entry.get("construction") or {}).get("task_id"),
                                      "promotion_states": dict(result["gates"])}
        if result["gates"]["integrity"] != "PASS":
            result["derived_state"] = "STALE_OR_UNRESOLVED"
            for gate in ("practice", "observations", "qrt", "construction", "release"):
                if result["gates"][gate] == "PASS":
                    result["gates"][gate] = "HOLD"
                    result["issues"].append({"gate": gate, "code": "UPSTREAM_INTEGRITY_HOLD", "detail": qid})
        result["dependency_trace"]["promotion_states"] = dict(result["gates"])
        return result

    def check(self, allow_partial_practice=False):
        report = {"schema": "smart-labelling-check-report/v2", "checker_version": VERSION,
                  "checker_artifact": {"path": str(Path(__file__).resolve()), "sha256": file_digest(__file__)},
                  "contract_path": str(self.path), "mode": "DETERMINISTIC_CONTRACT", "status": "PARTIAL",
                  "allow_partial_practice": allow_partial_practice, "inputs": self.artifacts, "records": [],
                  "checks_attempted": self.checks, "issues": [], "unsupported": ["Official authenticity and intellectual meaning require trusted independent human review", "Hashes alone do not establish historical immutability"],
                  "legacy_checks": "NOT_RUN"}
        try:
            self.contract = object_(read_json(self.path), "contract")
            self.artifacts[str(self.path)] = file_digest(self.path)
            require(self.contract.get("schema") == SCHEMA, "CONTRACT_SCHEMA", SCHEMA)
            refs = object_(self.contract.get("inputs"), "inputs")
            for name in ("sl1", "library", "vocabulary"):
                self.inputs[name] = object_(read_json(self.artifact(refs.get(name))), name)
            ranges = object_(self.inputs["vocabulary"].get("question_difficulty_score_ranges"), "rubric ranges")
            expected_ranges = {"D1": (0, 2), "D2": (3, 5), "D3": (6, 7), "D4": (8, 10)}
            require(set(ranges) == set(expected_ranges) and all(isinstance(ranges[key], dict) and
                    (ranges[key].get("min"), ranges[key].get("max")) == expected for key, expected in expected_ranges.items()),
                    "RUBRIC_POLICY_UNSUPPORTED", "The candidate supports the pinned G9 five-factor/D1-D4 policy; changed boundaries require an explicit versioned update")
            if "sl2" in refs:
                self.inputs["sl2"] = object_(read_json(self.artifact(refs["sl2"])), "sl2")
            for name in ("sl1", "sl2"):
                if name in self.inputs:
                    text_(self.inputs[name].get("labeller"), name + ".labeller")
            for target, label, field in (("library", "sl1", "library_ref"), ("vocabulary", "sl1", "vocabulary_ref"),
                                          ("sl1", "sl2", "sl1_ref"), ("vocabulary", "sl2", "rubric_ref")):
                if label in self.inputs:
                    declared = object_(self.inputs[label].get(field), label + "." + field)
                    require(self.resolve(declared.get("path")) == self.resolve(refs[target]["path"]),
                            "DECLARED_DEPENDENCY_MISMATCH", label + "." + field)
                    actual_version = self.inputs[target].get("version")
                    if "version" in declared and actual_version is not None:
                        require(declared["version"] == actual_version, "DEPENDENCY_VERSION_CHANGED", label + "." + field)
                    if "sha256" in declared:
                        require(hash_(declared["sha256"], "declared dependency") == hash_(refs[target]["sha256"], "contract dependency"),
                                "DECLARED_DEPENDENCY_MISMATCH", label + "." + field)
            for field in ("microtopics", "capabilities"):
                unique(self.inputs["library"].get(field, []), "id", "library." + field)
            sl1 = unique(self.inputs["sl1"].get("records"), "question_id", "sl1.records")
            sl2 = unique(self.inputs.get("sl2", {}).get("records", []), "question_id", "sl2.records")
            entries = unique(self.contract.get("records"), "question_id", "contract.records")
            report["adapters"] = {qid: (entry.get("source") or {}).get("adapter", "UNRESOLVED") for qid, entry in entries.items()}
            require(bool(sl1) and set(entries) == set(sl1), "COVERAGE_RECONCILIATION", "Contract must cover every SL1 record exactly once")
            require(not sl2 or set(sl2) == set(sl1), "ORPHANED_OR_MISSING_SL2", "SL2 and SL1 question IDs must match for this contract")
            for qid, record in sl1.items():
                try:
                    report["records"].append(self.record(entries[qid], record, sl2.get(qid), allow_partial_practice))
                except (Invalid, KeyError, TypeError, IndexError, AttributeError, ValueError) as exc:
                    report["records"].append({"question_id": qid, "gates": {g: "HOLD" if g == "integrity" else "NOT_RUN" for g in GATES},
                                              "issues": [{"gate": "integrity", "code": getattr(exc, "code", "INVALID_RECORD_SHAPE"), "detail": str(exc)}],
                                              "derived_state": "STALE_OR_UNRESOLVED"})
        except (Invalid, KeyError, TypeError, IndexError, AttributeError, ValueError) as exc:
            report["issues"].append({"code": getattr(exc, "code", "INVALID_CONTRACT_SHAPE"), "detail": str(exc)})
        report["gate_summary"] = {g: ("HOLD" if report["issues"] or not report["records"] or any(r["gates"][g] in {"HOLD", "NOT_RUN"} for r in report["records"]) else
                                             "NOT_APPLICABLE" if all(r["gates"][g] == "NOT_APPLICABLE" for r in report["records"]) else "PASS") for g in GATES}
        report["checks_attempted"] = [{"question_id": r["question_id"], "gate": gate, "status": status}
                                      for r in report["records"] for gate, status in r["gates"].items() if status != "NOT_RUN"]
        return report


def gate_passed(report, gate):
    return not report["issues"] and report["gate_summary"][gate] in {"PASS", "NOT_APPLICABLE"}
