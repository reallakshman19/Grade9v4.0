"""Browser regression for the five independent WPE Learn → Challenge teaching candidates."""
from __future__ import annotations
import http.server
import json
import pathlib
import re
import socketserver
import subprocess
import sys
import time
from difflib import SequenceMatcher
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
PORT=8768
URL=f"http://127.0.0.1:{PORT}/physics/wpe/learn-challenge.html"
MAP=ROOT/"physics/wpe/learn-challenge-source-map.json"
REVIEW=ROOT/"physics/wpe/learn-challenge-wpe01-review.json"
ART=ROOT/"wpe-learn-challenge-screenshots"
ART.mkdir(exist_ok=True)
SIZES=[(1280,800),(1024,768),(900,1280),(800,1280),(390,844)]

def check(expr, message):
    if not expr: raise AssertionError(message)

def corpus():
    data=json.loads(MAP.read_text(encoding="utf-8"))
    check(len(data["program"])==5,"Expected exactly five subtopic records")
    check(len({x["id"] for x in data["program"]})==5,"Duplicate IDs")
    check(data["auth"]["native_core1a"]=="NOT_ACCEPTED" and data["auth"]["native_core1b"]=="NOT_ACCEPTED","Gate status changed")
    required={"Q7","Q9","Q10","Q11","Q12"}
    check(required.issubset({r["id"] for r in data["source_flags"]}),"Source scan review flags incomplete")
    for row in data["program"]:
        a=row["core1a"]["authored_question"]
        b=row["core1b"]["authored_question"]
        def normalize(s):return re.sub(r"\s+"," ",re.sub(r"[\d.]+","#",s.casefold())).strip()
        score=SequenceMatcher(None,normalize(a),normalize(b)).ratio()
        check(score<0.7,f"Potential cosmetic A/B duplication {row['id']}: {score:.2f}")
        check(len(row["core1b"]["change_of_conditions"])>40, f"Transfer description missing: {row['id']}")
        check(row["core1b"]["option_count"]==4,f"Four choices expected: {row['id']}")
    review=json.loads(REVIEW.read_text(encoding="utf-8"))
    check(data["technical_review"]["status"]=="TECHNICAL_REMEDIATION_ONLY__ACADEMIC_HOLD","Academic review state changed")
    check(review["academic_acceptance"] is False,"WPE-01 must not be marked as academic acceptance")
    check(len(review["witnesses"])==5,"Expected five technical witnesses")
    check(all(r["gate_status"]["B4"]=="REVIEW_REQUIRED" for r in review["witnesses"]),"Fresh reconstruction wrongly accepted")
    check(review["construction_gate_status"]["B5"]=="LIMITED_TECHNICAL_EVIDENCE","Client-side lock must not count as verified first-attempt record")
    print("PASS: five distinct question pairs, technical review and academic holds")

def test(browser):
    for w,h in SIZES:
        context=browser.new_context(viewport={"width":w,"height":h},device_scale_factor=1)
        page=context.new_page()
        errors=[]
        page.on("pageerror", lambda e:errors.append(str(e)))
        result=page.goto(URL,wait_until="load",timeout=25000)
        check(result and result.status==200,f"Failed to load at {w}")
        cards=page.locator("article.lesson")
        check(cards.count()==5, f"Expected five lesson cards at {w}")
        check(page.locator(".guide-panel").count()==5 and page.locator(".challenge-panel").count()==5,"Missing Core1A / Core1B panels")
        check(page.locator(".topic-visual svg").count()==5,"Original explanatory diagrams missing")
        guide=page.locator(".guide-panel")
        check("single two-kilogram trolley" in guide.nth(1).locator("svg").get_attribute("aria-label"),"Momentum guide diagram still shows challenge carts")
        check("single straight potential-energy line" in guide.nth(3).locator("svg").get_attribute("aria-label"),"Potential guide diagram still previews challenge slopes")
        check("two carts separate from rest" in guide.nth(4).locator("figcaption").inner_text(),"Fragment guide diagram still previews moving parent")
        check("60 J" not in guide.nth(2).locator("svg").text_content(),"Core1A visual leaks ridge answer")
        check(not errors,f"JS errors at {w}: {errors}")
        wide=page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(wide<=2,f"Horizontal overflow {wide}px at {w}")
        card=cards.first
        check(card.locator(".solution-area").inner_text().strip()=="","Answer in initial live DOM")
        check(card.locator('[data-action="hint"]').is_disabled(),"Hints should initially be locked")
        check(card.locator('[data-action="solution"]').is_disabled(),"Solution should initially be locked")
        card.locator('[data-action="lock"]').click()
        check("Choose an answer" in card.locator(".feedback").inner_text(),"Must require an answer")
        card.locator('input[type=radio]').first.check()
        card.locator('[data-action="lock"]').click()
        check("8 characters" in card.locator(".feedback").inner_text(),"Must require reasoning")
        card.locator(".reason").fill("Both resistance forces oppose motion, so their work is negative.")
        card.locator('[data-action="lock"]').click()
        check(card.locator('[data-action="lock"]').is_disabled(),"Attempt not locked")
        check(card.locator('[data-action="hint"]').is_enabled(),"Hint 1 locked after attempt")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:work-sign')") is not None,"Locked attempt not saved locally")
        page.reload(wait_until="load")
        check(card.locator('[data-action="lock"]').is_disabled(),"First attempt lock failed to survive reload")
        check("Both resistance forces" in card.locator(".reason").input_value(),"Reason failed to survive reload")
        check(card.locator('[data-action="hint"]').is_enabled(),"Hints not restored after reload")
        check(card.locator(".solution-area").is_hidden(),"Solution must be hidden")
        card.locator('[data-action="hint"]').click()
        check(card.locator(".hint-area p").count()==1,"Hint 1 missing")
        page.reload(wait_until="load")
        check(card.locator(".hint-area p").count()==1,"Hint 1 lost or duplicated after reload")
        check(card.locator('[data-action="solution"]').is_disabled(),"Answer unlocked too early")
        card.locator('[data-action="hint"]').click()
        check(card.locator(".hint-area p").count()==2,"Hint 2 missing")
        check(card.locator('[data-action="solution"]').is_enabled(),"Solution should be available after both hints")
        card.locator('[data-action="solution"]').click()
        check(card.locator(".solution-area").is_visible(),"Worked check not revealed")
        check("−32 J" in card.locator(".solution-area").inner_text(),"Incorrect work solution")
        check(card.locator(".choice input:checked").is_disabled(),"First attempt answer should remain locked")
        page.reload(wait_until="load")
        check(card.locator(".solution-area").is_visible(),"Solution reveal was not restored")
        check("Changed-condition reflection" in card.locator(".solution-area").inner_text(),"Missing transfer reflection")
        # verify other cards remain unmodified until user interacts with each
        for i in range(1,5):
            row=cards.nth(i)
            check(row.locator('[data-action="lock"]').is_enabled(),f"Card {i+1} unexpectedly locked")
            check(row.locator(".solution-area").is_hidden(),f"Card {i+1} accidentally leaked solution")
        if w in (1280,1024,900,800):
            page.screenshot(path=str(ART/f"learn-challenge-{w}x{h}.png"),full_page=False)
        card.locator('[data-action="reset"]').click()
        check(card.locator('[data-action="lock"]').is_enabled(),"Clear saved attempt did not reset form")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:work-sign')") is None,"Clear saved attempt left local record behind")
        check(card.locator(".solution-area").is_hidden(),"Clear saved attempt left answer visible")
        print(f"PASS: {w}x{h} layout, interaction, answer protection")
        context.close()

def main():
    corpus()
    server=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        import urllib.request
        for _ in range(60):
            try: urllib.request.urlopen(URL,timeout=0.4);break
            except Exception: time.sleep(.2)
        else: raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try:test(browser)
            finally:browser.close()
        print("PASS: Five authored pairs and five viewport browser checks.")
    finally:
        server.terminate();server.wait(timeout=8)

if __name__=="__main__":main()
