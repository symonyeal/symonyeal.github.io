"""Certificates for the built site: it is the image of content/ under build.py, its local links
resolve, it carries no private contact detail, and the PDF transcribes the résumé."""
import re
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

import pypdf
import build

SITE = build.SITE
PHONE = re.compile(r"\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")  # North American number
norm = lambda s: re.sub(r"\s+", " ", s).replace("’", "'")


class Refs(HTMLParser):
    def __init__(s):
        super().__init__(); s.refs, s.ids = [], set()

    def handle_starttag(s, tag, at):
        at = dict(at)
        if "id" in at: s.ids.add(at["id"])
        s.refs += [at[k] for k in ("href", "src") if k in at]
        s.refs += [u.split()[0] for u in at.get("srcset", "").split(",") if u.strip()]


def parse(f):
    r = Refs(); r.feed(f.read_text(encoding="utf-8")); return r


def test_pages_are_built_from_content():
    for k, v in build.pages().items():
        assert (SITE / k).read_text(encoding="utf-8") == v, f"{k} is stale: run python build.py"


def test_local_links_resolve():
    pages = {f.name: parse(f) for f in SITE.glob("*.html")}
    for name, r in pages.items():
        for u in r.refs:
            x = urlsplit(u)
            if x.scheme or u.startswith("//"): continue
            path = unquote(x.path) or name
            target = SITE / (path if not path.endswith("/") else path + "index.html")
            if path in ("./", "."): target = SITE / "index.html"
            assert target.exists(), f"{name}: {u}"
            if x.fragment:
                assert x.fragment in pages[target.name].ids, f"{name}: #{x.fragment}"


def test_every_project_is_complete():
    for p in build.PR:
        assert p["subject"] in build.SUBJECTS
        assert p["links"] and all(u.startswith("https://") for _, u in p["links"])
        assert any("github.com/symonyeal/" in u for _, u in p["links"])
        if p.get("featured"): assert len(p["stat"]) == 2 and all(p["stat"])
        if "formula" not in p:
            assert p["image_alt"] and all((SITE / "img" / f"{p['slug']}-{n}.webp").exists() for n in (600, 1200))


def test_no_private_contact_detail():
    for f in SITE.glob("*.html"):
        assert not PHONE.search(re.sub(r"<[^>]+>", " ", f.read_text(encoding="utf-8"))), f
    assert not PHONE.search(pdf_text())


def pdf_text():
    return norm(" ".join(pg.extract_text() for pg in pypdf.PdfReader(SITE / build.PDF).pages))


def test_pdf_transcribes_resume():
    t = pdf_text()
    assert len(pypdf.PdfReader(SITE / build.PDF).pages) <= 2
    for x in build.CV["experience"] + build.CV["education"]:
        for k in ("title", "degree", "org", "dates"):
            if k in x: assert norm(x[k]) in t, x[k]
    for x in build.CV["experience"]:
        for pt in x["points"]:
            assert norm(pt)[:40] in t, pt
