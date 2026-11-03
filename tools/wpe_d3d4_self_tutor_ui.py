"""Chromium QA for four source-grounded WPE six-stage student practice journeys."""
from __future__ import annotations

import http.server
import json
import pathlib
import threading
from functools import partial

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = "/physics/wpe/d3d4-self-tutor.html"
VIEWPORTS = [(1280, 800), (1024, 768), (900, 1280), (800, 1280), (390, 844)]


def check(ok, msg):
    if not ok:
        raise AssertionError(msg)


def local_server():
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, "http://127.0.0.1:" + str(server.server_port)


def saved_state(page, lesson):
    key = "g9:wpe:d3d4:self-tutor:v1:" + lesson
    return page.evaluate("(key) => JSON.parse(localStorage.getItem(key))", key)


def root_for(page, lesson):
    return page.locator('[data-stage-root="' + lesson + '"]')


def fill_stage_one(page, lesson, answer):
    root = root_for(page, lesson)
    check(root.locator(".stage-card h4").inner_text() == "1. Predict", lesson+" predict stage missing")
    check(root.locator(".worked").count() == 0, lesson+" answer leaked before attempt")
    root.locator('[data-action="save-prediction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "1. Predict", lesson+" blank prediction unlocked")
    root.locator("textarea").fill("I think the moving object gains energy, but I want to check the forces.")
    root.locator('[data-action="save-prediction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "2. Attempt", lesson+" attempt not available")
    check(root.locator(".worked").count() == 0, lesson+" worked answer shown too early")
    root.locator('[data-action="lock-attempt"]').click()
    check(root.locator(".stage-card h4").inner_text() == "2. Attempt", lesson+" blank explanation unlocked")
    root.locator('[data-input="reason"]').fill(answer)
    if lesson == "C01":
        root.locator('[data-input="motor"]').select_option(label="Positive (+)")
        root.locator('[data-input="friction"]').select_option(label="Negative (−)")
        root.locator('[data-input="gravity"]').select_option(label="Positive (+)")  # deliberately incorrect reasoning
        root.locator('[data-input="normal"]').select_option(label="Zero (0)")
        root.locator('[data-input="netWork"]').fill("39")
        root.locator('[data-input="topSpeed"]').fill("5")
    elif lesson == "C02":
        root.locator('[data-input="boundary"]').select_option(label="At the far end of the rough strip")  # incorrect
        root.locator('[data-input="springEnergy"]').fill("1")
        root.locator('[data-input="finalSpeed"]').fill("1")
    elif lesson == "C03":
        root.locator('[data-input="powerMeaning"]').select_option(label="The force is always 18 N")  # incorrect
        root.locator('[data-input="initialEnergy"]').fill("0")  # forgot initial energy
        root.locator('[data-input="energyAt2"]').fill("36")
        root.locator('[data-input="speedAt2"]').fill("5")
        root.locator('[data-input="energyGraph"]').select_option(label="Straight rising line")
        root.locator('[data-input="speedGraph"]').select_option(label="Straight rising line")  # misconception
    elif lesson == "C04":
        root.locator('[data-input="massPerMetre"]').fill("0.5")
        root.locator('[data-input="startMass"]').fill("4")  # used total rope mass
        root.locator('[data-input="startDepth"]').fill("4")
        root.locator('[data-input="endMass"]').fill("4")
        root.locator('[data-input="helperWork"]').fill("80")
        root.locator('[data-input="modelChoice"]').select_option(label="The whole 4 kg rope in both states")
    else:
        raise AssertionError("Unknown topic " + lesson)
    root.locator('[data-action="lock-attempt"]').click()
    check(root.locator(".stage-card h4").inner_text() == "3. Reconstruct", lesson+" first attempt not committed")
    check(root.locator(".worked").count() == 1, lesson+" worked reconstruction not available")
    state = saved_state(page, lesson)
    check(state["first"]["reason"] == answer, lesson+" first answer missing from storage")
    check(state["stage"] == 2, lesson+" stage not stored")
    check(root.locator(".snapshot").inner_text().find(answer) >= 0, lesson+" first model not displayed")
    return state["first"]


def finish_stages(page, lesson, first):
    root = root_for(page, lesson)
    page.reload(wait_until="load")
    root = root_for(page, lesson)
    check(root.locator(".stage-card h4").inner_text() == "3. Reconstruct", lesson+" first attempt lost after reload")
    check(saved_state(page, lesson)["first"] == first, lesson+" first snapshot changed after reload")
    check(root.locator(".rubric li").count() == 4, lesson+" reconstruction rubric incomplete")
    root.locator("[data-rubric]").first.check()
    root.locator('[data-action="save-reconstruction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "4. Diagnose", lesson+" diagnosis missing")
    check(root.locator(".worked").count() == 0, lesson+" reconstruction answer repeated unnecessarily")
    root.locator('[data-input="diagnosis"]').select_option(index=1)
    root.locator("[data-input$=diagnosisWhy]").fill("My first physics model needs a different boundary or work sign.")
    root.locator('[data-action="save-diagnosis"]').click()
    check(root.locator(".stage-card h4").inner_text() == "5. Repair", lesson+" repair missing")
    root.locator("[data-input$='-repair']").fill("I corrected the first wrong model choice and now use the right energy ledger.")
    root.locator('[data-action="save-repair"]').click()
    check(root.locator(".stage-card h4").inner_text() == "6. Boundary test", lesson+" boundary stage missing")
    check(root.locator(".worked").count() == 0, lesson+" boundary worked check visible before attempt")
    root.locator("[data-input$='-boundary']").fill("I need to check whether energy remains positive at the new endpoint.")
    root.locator('[data-action="save-boundary"]').click()
    check(root.locator(".response-done").count() == 1, lesson+" completion missing")
    check(root.locator(".worked").count() == 1, lesson+" boundary worked check missing")
    state = saved_state(page, lesson)
    check(state["stage"] == 5 and bool(state["boundary"]), lesson+" boundary answer not saved")
    check(state["first"] == first, lesson+" original was overwritten by repair")
    check(bool(state["repair"]) and isinstance(state["diagnosis"], dict), lesson+" diagnosis/repair not stored")
    root.locator('[data-action="review-history"]').click()
    check(root.locator(".history .snapshot").count() == 2, lesson+" first/repair history not independently visible")
    check(first["reason"] in root.locator(".history").inner_text(), lesson+" first reasoning missing in history")
    check("I corrected" in root.locator(".history").inner_text(), lesson+" repair missing in history")
    return state


def run_viewport(browser, width, height, base):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    try:
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        response = page.goto(base+PATH, wait_until="load")
        check(response is not None and response.status == 200, "Self-tutor page did not load")
        check(page.locator("article.unit").count() == 4, "Four lessons missing")
        check(page.locator(".guide-steps").count() == 4, "Core1A guides missing")
        check(page.locator(".stage-root .step-list li").count() == 24, "All six stages not listed for four lessons")
        check(page.locator("body").inner_text().find("This page does not grade explanations") != -1, "Non-grading learner note missing")
        check(page.locator("#overall-count").inner_text() == "0 of 4 challenges completed", "Initial progress incorrect")
        check(not errors, "JavaScript error on load: "+str(errors))
        check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 3"),
              "Horizontal page overflow at "+str(width))

        # Four distinct first attempts; each deliberately includes a plausible conceptual mistake;
        # there is no automatic evaluation of the child's free-text explanation.
        first_c01 = fill_stage_one(page, "C01", "I counted the motor and gravity as helping uphill, maybe 39 joules.")
        check(saved_state(page, "C02") is None, "C01 saved the other topic unexpectedly")
        finish_stages(page, "C01", first_c01)
        check(page.locator("#overall-count").inner_text() == "1 of 4 challenges completed", "First completion not counted")
        first_c02 = fill_stage_one(page, "C02", "I think the spring might keep pushing into the rough strip.")
        finish_stages(page, "C02", first_c02)
        check(page.locator("#overall-count").inner_text() == "2 of 4 challenges completed", "Second completion not counted")
        first_c03 = fill_stage_one(page, "C03", "I think 18 watts means constant force and each second gives the same speed increase.")
        check("Kinetic energy" in root_for(page, "C03").locator(".worked").inner_text()
              or "kinetic energy" in root_for(page, "C03").locator(".worked").inner_text(),
              "C03 reconstruction does not explain power/energy relationship")
        finish_stages(page, "C03", first_c03)
        check(page.locator("#overall-count").inner_text() == "3 of 4 challenges completed",
              "Third completion not counted")
        first_c04 = fill_stage_one(page, "C04", "I used the whole four kilograms in both rope pictures instead of changing the hanging mass.")
        check("−40 J" in root_for(page, "C04").locator(".worked").inner_text(),
              "C04 worked model missing initial hanging potential")
        finish_stages(page, "C04", first_c04)
        check(page.locator("#overall-count").inner_text() == "4 of 4 challenges completed",
              "Fourth completion not counted")
        page.reload(wait_until="load")
        check(page.locator("#overall-count").inner_text() == "4 of 4 challenges completed", "Completed progress not restored")
        for lesson, initial in (("C01",first_c01),("C02",first_c02),("C03",first_c03),("C04",first_c04)):
            check(saved_state(page, lesson)["first"] == initial,
                  lesson+" first reasoning was modified after completing all four lessons")
        check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 3"),
              "Page overflow after completion at "+str(width))
        check(not errors, "JavaScript runtime errors: "+str(errors))

        page.on("dialog", lambda d: d.accept())
        root_for(page, "C01").locator('[data-action="reset"]').click()
        check(saved_state(page, "C01") is None, "C01 reset did not clear local attempt")
        check(saved_state(page, "C02")["first"] == first_c02, "Reset of C01 cleared C02")
        check(page.locator("#overall-count").inner_text() == "3 of 4 challenges completed", "Reset progress incorrect")
        check(saved_state(page, "C03")["first"] == first_c03 and saved_state(page, "C04")["first"] == first_c04,
              "Resetting C01 unexpectedly cleared new C03/C04 records")
        print("PASS: %sx%s C01–C04 all stages, independent first tries, repair, boundaries, persistence, reset" % (width,height))
    finally:
        context.close()


def main():
    server, base = local_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for width,height in VIEWPORTS:
                    run_viewport(browser,width,height,base)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
