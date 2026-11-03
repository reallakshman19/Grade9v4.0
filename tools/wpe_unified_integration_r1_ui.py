"""Chromium student-journey acceptance checks for unified WPE integration.

Browser assertions are mechanical only, not evidence of real child comprehension.
"""
from __future__ import annotations

from functools import partial
import http.server
import threading
from playwright.sync_api import sync_playwright

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = ((1280, 800), (390, 844))
CASES = (("F01", "EX-M97", "Net accelerating force only", "appliedPower"),
         ("F02", "EX-N39", "Only the uphill work ledger", "mu"),
         ("F03", "WEP07-01", "Spring elastic energy only", "turning"))


def require(value, message):
    if not value:
        raise AssertionError(message)


def server():
    svc = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    )
    svc.daemon_threads = True
    threading.Thread(target=svc.serve_forever, daemon=True).start()
    return svc, "http://127.0.0.1:" + str(svc.server_port)


def state(page, key):
    return page.evaluate("(k)=>JSON.parse(localStorage.getItem(k))", key)


def source_attempt(page, source, commit):
    page.goto(page.context._wpe_base + "/preview/question-status.html?question=" + source)
    require(page.locator(".qtitle").inner_text() == source, "Lost exact source question " + source)
    require(page.locator("#solution-container .solution").count() == 0, "Answer leaked on source open")
    options = page.locator('input[name="answer-option"]')
    if options.count():
        options.nth(1).check()
        check = lambda: require(options.nth(1).is_checked(), "Source draft selection lost")
    else:
        page.locator("#free-answer").fill("First uncommitted reasoning: track the force and energy signs.")
        check = lambda: require("First uncommitted reasoning" in page.locator("#free-answer").input_value(),
                                "Source written draft lost")
    page.reload()
    check()
    if commit:
        page.locator("#commit").click()
        require(page.locator("#commit").is_disabled(), "Source attempt was not committed")
        saved = state(page, "g9:wpe:core2:attempt:v1:" + source)
        require(saved and saved["committed"] and saved["first"], "Committed source first attempt lost")
        return saved
    saved = state(page, "g9:wpe:core2:attempt:v1:" + source)
    require(saved is not None and not saved["committed"], "Source draft not saved")
    return saved


def run_original_six_stages(page, lesson):
    root = page.locator('[data-stage-root="' + lesson + '"]')
    require(root.locator(".worked").count() == 0, lesson + " primary reconstruction exposed first")
    root.locator('[data-field="prediction"]').fill("I need a model for the changing physical phase.")
    root.locator('[data-action="prediction"]').click()
    root.locator('[data-field="model"]').select_option(label="I'm not sure yet")
    root.locator('[data-field="reason"]').fill("First independent attempt: decide which force or energy changes.")
    root.locator('[data-action="attempt"]').click()
    require(root.locator(".stage-card h3").inner_text() == "3. Reconstruct", lesson + " primary attempt failed")
    primary = state(page, "g9:wpe:focused:v1:" + lesson)["first"]
    root.locator('[data-action="reconstruct"]').click()
    root.locator('[data-diagnosis]').select_option("model")
    root.locator('[data-field="why"]').fill("My first model was uncertain.")
    root.locator('[data-action="diagnose"]').click()
    root.locator('[data-field="repair"]').fill("The force owner and physical phases determine the work ledger.")
    root.locator('[data-action="repair"]').click()
    require(root.locator(".stage-card .worked").count() == 0, "Primary boundary check revealed too soon")
    root.locator('[data-field="why"]').fill("One condition changes the energy transferred during a phase.")
    root.locator('[data-action="boundary"]').click()
    require(root.locator(".stage-card .worked").count() == 1, "Primary boundary not checked after attempt")
    require(root.get_by_text("Try another challenge (optional)").count() >= 1,
            "Optional transfer was not offered after primary")
    return primary


def run_transfer(page, lesson, source, wrong_model, wrong_field):
    key1 = "g9:wpe:focused:v1:" + lesson
    key2 = key1 + "-transfer55"
    original = state(page, key1)
    page.goto(page.context._wpe_base + "/physics/wpe/focused-journeys.html?question="
              + source + "&variant=transfer55#" + lesson)
    page.locator("#source-journey:not([hidden])").wait_for()
    root = page.locator('[data-stage-root="' + lesson + '-transfer55"]')
    require(root.locator(".worked").count() == 0, "Transfer worked result exposed before first attempt")
    guide = page.locator(".guide")
    require(guide.locator("svg").count() == 1, "Original lesson guide not reused for transfer")
    require(page.evaluate("document.documentElement.scrollWidth <= innerWidth+3"),
            "Transfer page horizontally overflows")
    root.locator('[data-field="prediction"]').fill("My model decision is not the same as copying the example.")
    root.locator('[data-action="prediction"]').click()
    reason = "I independently selected " + wrong_model + " before the reconstruction."
    root.locator('[data-field="model"]').select_option(label=wrong_model)
    root.locator('[data-field="' + wrong_field + '"]').fill("999")
    root.locator('[data-field="reason"]').fill(reason)
    for i in range(1, 4):
        root.locator('[data-action="hint"]').click()
        require(root.locator(".hint-list li").count() == i, "Transfer hints not staged")
        require(root.locator(".worked").count() == 0, "Transfer hint leaked reconstruction")
        require(root.locator('[data-field="reason"]').input_value() == reason, "Hints erased first reasoning")
    page.reload()
    page.locator("#source-journey:not([hidden])").wait_for()
    require(root.locator(".hint-list li").count() == 3, "Transfer hints not restored")
    require(root.locator('[data-field="reason"]').input_value() == reason, "Transfer draft lost on reload")
    root.locator('[data-action="attempt"]').click()
    require(root.locator(".stage-card h3").inner_text() == "3. Reconstruct", "Transfer did not commit first attempt")
    first = state(page, key2)["first"]
    require(first["answers"]["reason"] == reason and first["hintsUsed"] == 3, "Transfer first snapshot wrong")
    require("Review this step" in root.locator(".assessment").inner_text(),
            "Incorrect-model-specific feedback missing")
    require(state(page, key1) == original, "Optional transfer overwrote primary state")
    root.locator('[data-action="reconstruct"]').click()
    require(root.get_by_text("Specific reasoning traps to examine").count() == 1,
            "PR55 diagnoses not incorporated")
    root.locator('[data-diagnosis]').select_option("model")
    root.locator('[data-field="why"]').fill("I used the wrong initial model, rather than the phase ledger.")
    root.locator('[data-action="diagnose"]').click()
    require(reason in root.locator(".snapshot").inner_text(), "Transfer first attempt hidden during repair")
    root.locator('[data-field="repair"]').fill("I will rebuild the phase-specific ledger and explain each assumption.")
    root.locator('[data-action="repair"]').click()
    require(root.locator(".stage-card .worked").count() == 0, "Transfer boundary answer exposed too soon")
    root.locator('[data-field="why"]').fill("The changed condition requires a new physical balance and check.")
    page.reload()
    root = page.locator('[data-stage-root="' + lesson + '-transfer55"]')
    require("changed condition" in root.locator('[data-field="why"]').input_value(),
            "Uncommitted boundary draft lost after refresh")
    root.locator('[data-action="boundary"]').click()
    require(root.locator(".stage-card .worked").count() == 1, "Transfer boundary reconstruction missing")
    require(state(page, key1) == original, "Transfer boundary overwrote primary state")
    require(state(page, key2)["first"] == first, "Transfer repair overwrote transfer first attempt")
    page.locator("#source-return").click()
    require(page.locator(".qtitle").inner_text() == source, "Transfer returned wrong source question")
    require(page.locator("#solution-container .solution").count() == 0,
            "Returning from transfer automatically exposed author proposal")
    return first


def case(browser, base, width, height):
    context = browser.new_context(viewport={"width": width, "height": height},
                                  device_scale_factor=1)
    context._wpe_base = base
    try:
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(base + "/physics/wpe/index.html")
        require(page.get_by_role("heading", name="Learn → Challenge").count() == 1,
                "Chapter gateway not singular")
        require(page.get_by_role("heading", name="Practice my skills").count() == 1,
                "Chapter practice tile missing")
        page.goto(base + "/physics/wpe/learn-challenge.html")
        page.locator("#skill-links a").first.wait_for()
        require(page.locator("#skill-links a").count() == 16,
                "Not all C/E/F direct skill destinations offered")
        require(page.locator("#question-plan .primary-link").count() == 0,
                "Question-less gateway guessed a route")
        page.goto(base + "/physics/wpe/question-bank.html?question=EX-M79")
        page.wait_for_url("**/preview/question-status.html?question=EX-M79")
        page.locator('#interactive-lesson-links a[href*="d3d4-self-tutor.html?question=EX-M79#C03"]').wait_for()
        page.locator('input[name="answer-option"]').first.check()
        page.reload()
        require(page.locator('input[name="answer-option"]').first.is_checked(), "EX-M79 draft lost")
        page.locator("#commit").click()
        page.locator('#interactive-lesson-links a[href*="d3d4-self-tutor.html?question=EX-M79#C03"]').click()
        page.locator("#source-journey-return").wait_for(state="visible")
        require(page.url.endswith("d3d4-self-tutor.html?question=EX-M79#C03"),
                "EX-M79 did not open C03 with preserved source ID")
        page.locator("#source-journey-return").click()
        require(page.locator(".qtitle").inner_text() == "EX-M79", "C03 return lost source")
        require(page.locator("#commit").is_disabled(), "Committed EX-M79 attempt was lost")
        require(page.locator("#solution-container .solution").count() == 0,
                "Original author answer leaked on C03 return")
        page.reload()
        require(page.locator("#solution-container .solution").count() == 0,
                "Original answer leaked after reload")
        page.locator("#reveal").click()
        require(page.locator("#solution-container .solution").count() == 1,
                "Explicit reveal did not show author proposal")
        page.reload()
        require(page.locator("#solution-container .solution").count() == 0,
                "Author proposal reappeared automatically after reload")
        page.once("dialog", lambda dlg: dlg.accept())
        page.locator("#restart-source").click()
        require(state(page, "g9:wpe:core2:attempt:v1:EX-M79") is None,
                "Per-question Start again did not clear saved state")
        require(not page.locator('input[name="answer-option"]').first.is_checked(),
                "Start again retained an old selection")
        page.goto(base + "/physics/wpe/learn-challenge.html#practice-controls")
        page.locator("#clear-saved-practice").wait_for()
        page.once("dialog", lambda dlg: dlg.accept())
        page.locator("#clear-saved-practice").click()
        require(page.locator("#saved-practice-status").inner_text().startswith("Saved WPE practice cleared"),
                "Clear saved practice was not confirmed")
        require(not errors, "Unexpected JS exceptions: " + repr(errors))
        print("PASS source draft, commit, explicit reveal, reload, per-question reset and clear at", width)
    finally:
        context.close()


def full_case(browser, base, width, height):
    context = browser.new_context(viewport={"width":width, "height":height})
    context._wpe_base = base
    try:
        page=context.new_page()
        errors=[]
        page.on("pageerror",lambda exc:errors.append(str(exc)))
        for lesson, source, wrong_model, wrong_field in CASES:
            original_source=source_attempt(page, source, commit=True)
            page.goto(base + "/physics/wpe/focused-journeys.html?question=" + source + "#" + lesson)
            page.locator("#source-journey:not([hidden])").wait_for()
            primary=run_original_six_stages(page, lesson)
            run_transfer(page, lesson, source, wrong_model, wrong_field)
            require(state(page, "g9:wpe:focused:v1:" + lesson)["first"] == primary,
                    lesson + " primary state mutated")
            require(state(page, "g9:wpe:core2:attempt:v1:" + source)["first"] == original_source["first"],
                    lesson + " source commit mutated")
            require(page.locator("#commit").is_disabled(), lesson + " source commit vanished on return")
            require(page.locator("#solution-container .solution").count() == 0,
                    lesson + " original answer revealed")
            require(page.locator("iframe").count() == 0, "Iframe found on student return")
        page.goto(base + "/physics/wpe/study-bridge.html?question=EX-M11&lesson=C05")
        page.wait_for_url("**/d3d4-self-tutor.html?question=EX-M11#C05")
        require(page.locator("#source-journey-return").is_visible(),
                "Older direct bridge link did not redirect to verified lesson")
        page.goto(base + "/physics/wpe/study-bridge.html?question=UNKNOWN-ID&lesson=C05")
        require(page.locator("#destination").get_attribute("href") == "learn-challenge.html",
                "Unknown source was given a guessed lesson")
        require(not errors, "Unexpected JS exceptions: " + repr(errors))
        print("PASS three F optional transfers, independent source/first attempts, saved boundaries and no-frame redirect at", width)
    finally:
        context.close()


def main():
    svc, base = server()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for width, height in VIEWPORTS:
                    case(browser, base, width, height)
                    full_case(browser, base, width, height)
            finally:
                browser.close()
    finally:
        svc.shutdown()
        svc.server_close()


if __name__ == "__main__":
    main()
