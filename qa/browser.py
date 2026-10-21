"""Browser checks against a running server (default http://127.0.0.1:8765/), in Microsoft Edge.

    python -m http.server 8765 --bind 127.0.0.1 --directory site
    python qa/browser.py [base-url] [--external]

Checks, at widths 360, 390, 768 and 1440 and in both colour schemes: no horizontal scroll; every
nav target exists; the gallery filter shows exactly the cards of each subject; the PDF link returns
a PDF. --external also requests every outbound link. Screenshots go to qa/out/.
"""
import sys, urllib.error, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

base = next((x for x in sys.argv[1:] if x.startswith("http")), "http://127.0.0.1:8765/")
out = Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
fail = []


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok: fail.append(msg)


with sync_playwright() as pw:
    b = pw.chromium.launch(channel="msedge")
    for W, H in [(360, 780), (390, 844), (768, 1024), (1440, 900)]:
        for scheme in ["light", "dark"]:
            pg = b.new_page(viewport={"width": W, "height": H}, color_scheme=scheme)
            for page in ["", "resume.html"]:
                pg.goto(base + page, wait_until="networkidle")
                pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
                pg.wait_for_load_state("networkidle")
                over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(over <= 0, f"{W}px {scheme} /{page}: horizontal overflow {over}px")
                if scheme == "light" or W in (390, 1440):
                    pg.screenshot(path=out / f"{(page or 'index').split('.')[0]}-{W}-{scheme}.png", full_page=True)
            pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(base, wait_until="networkidle")
    for h in pg.eval_on_selector_all(".top nav a", "as => as.map(a => a.getAttribute('href'))"):
        if "#" in h:
            check(pg.locator(h[h.index("#"):]).count() == 1, f"nav target {h}")
    n = pg.locator(".card").count()
    for btn in pg.locator(".filter button").all():
        s = btn.get_attribute("data-subject"); btn.click()
        shown = pg.locator(".card:not([hidden])")
        want = n if s == "" else pg.locator(f'.card[data-subject="{s}"]').count()
        check(shown.count() == want > 0 and btn.get_attribute("aria-pressed") == "true",
              f"filter '{s or 'All'}' shows {shown.count()} of {n}")
    pg.locator('.filter button[data-subject=""]').click()
    pg.locator("details summary").first.click()
    check(pg.locator("details[open]").count() == 1, "card details open on tap")
    r = pg.request.get(base + "Saimon-Islam-Resume.pdf")
    check(r.ok and r.headers.get("content-type") == "application/pdf" and r.body()[:4] == b"%PDF", "résumé PDF downloads")
    check(pg.locator("img:not([alt])").count() == 0, "every image has alt text")
    hrefs = sorted(set(pg.eval_on_selector_all("a[href^=http]", "as => as.map(a => a.href)")))
    b.close()

if "--external" in sys.argv:
    for u in hrefs:
        if "linkedin.com" in u:  # LinkedIn answers 999 to non-browser clients; checked by hand
            print("skip " + u); continue
        try:
            q = urllib.request.Request(u, method="GET", headers={"User-Agent": "Mozilla/5.0 link-check"})
            code = urllib.request.urlopen(q, timeout=30).status
        except (urllib.error.URLError, TimeoutError) as x:
            code = getattr(x, "code", repr(x))
        check(code == 200, f"{code} {u}")

print(f"\n{len(fail)} failure(s)")
sys.exit(1 if fail else 0)
