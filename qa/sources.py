"""Network checks for the published cards (run in CI, standard library only).

    python qa/sources.py            # card numbers against origin READMEs, then outbound links
    python qa/sources.py --cards    # only the cards
    python qa/sources.py --links    # only the links

A card number is a number in a project's headline. It must appear in the README of the project's
repository (HEAD); a number that does not is listed and the exit code is 1. Every outbound link in
site/*.html must answer 200; LinkedIn answers 999 to non-browser clients and is skipped.

Legend
  H : headline    N : numbers in H    T : origin README text    GH : repository path in a project's links
"""
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
GH = re.compile(r"^https://github\.com/(symonyeal/[\w.-]+)/?$")


def numbers(h):
    """Numbers of a headline as plain strings (no thousands commas); calendar years are not card numbers."""
    N = {m.rstrip(",").replace(",", "") for m in NUM.findall(h)}
    return sorted(n for n in N if not re.fullmatch(r"(19|20)\d\d", n))


def missing(h, T):
    """Card numbers that the README text does not contain."""
    t = T.replace(",", "")
    return [n for n in numbers(h) if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d]|\.\d)", t)]


def get(u):
    q = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 card-check"})
    return urllib.request.urlopen(q, timeout=30)


def cards():
    bad = 0
    for p in build.PR:
        gh = next((m[1] for _, u in p["links"] if (m := GH.match(u))), None)
        if not gh:
            continue
        try:
            T = get(f"https://raw.githubusercontent.com/{gh}/HEAD/README.md").read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as x:
            print(f"FAIL {p['slug']}: README of {gh} not readable: {x}")
            bad += 1
            continue
        m = missing(p["headline"], T)
        print(f"{'FAIL' if m else 'ok  '} {p['slug']}: " + (f"not in {gh} README: {', '.join(m)}" if m else "card numbers found"))
        bad += bool(m)
    return bad


def links():
    H = re.compile(r'href="(https?://[^"]+)"')
    U = sorted({u for f in build.SITE.glob("*.html") for u in H.findall(f.read_text(encoding="utf-8"))})
    bad = 0
    for u in U:
        if "linkedin.com" in u:
            print("skip " + u)
            continue
        try:
            code = get(u).status
        except (urllib.error.URLError, TimeoutError) as x:
            code = getattr(x, "code", repr(x))
        print(("ok   " if code == 200 else "FAIL ") + f"{code} {u}")
        bad += code != 200
    return bad


if __name__ == "__main__":
    a = sys.argv[1:]
    bad = (cards() if "--links" not in a else 0) + (links() if "--cards" not in a else 0)
    print(f"\n{bad} failure(s)")
    sys.exit(1 if bad else 0)
