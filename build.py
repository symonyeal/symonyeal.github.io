"""Build the site from content/*.toml.

    python build.py            content → site/index.html, site/resume.html
    python build.py --render   also site/Saimon-Islam-Resume.pdf and site/og.png (needs Microsoft Edge)

The pages are a function of the content files alone, so `tests/` can rebuild and compare.
"""
import sys, tomllib
from html import escape as e
from pathlib import Path

R = Path(__file__).parent
SITE = R / "site"
SUBJECTS = ["Optimization", "Applied statistics", "Discrete mathematics", "Simulation and games"]
PDF = "Saimon-Islam-Resume.pdf"


def load(name):
    return tomllib.loads((R / "content" / f"{name}.toml").read_text(encoding="utf-8"))


P, CV, PR = load("profile"), load("resume"), load("projects")["project"]


def a(url, label, cls=""):
    ext = url.startswith("http")
    return (f'<a href="{e(url)}"' + (f' class="{cls}"' if cls else "")
            + (' rel="noopener"' if ext else "") + f">{e(label)}</a>")


def head(title, desc, path):
    url = P["site"] + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{P['site']}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/source-serif-4.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="./">{e(P['name'])}</a>
<nav aria-label="Main"><ul>
<li><a href="./#work">Work</a></li><li><a href="./#projects">Projects</a></li><li><a href="./#experience">Experience</a></li><li><a href="resume.html">Résumé</a></li><li><a href="./#contact">Contact</a></li>
</ul></nav>
</div></header>
"""


def foot():
    return f"""<footer class="foot"><div class="wrap">
<p>{e(P['name'])} · {a(P['github'], 'GitHub')} · {a(P['linkedin'], 'LinkedIn')} · {a('mailto:' + P['email'], P['email'])}</p>
<p>Static site; source at {a(P['github'] + '/symonyeal.github.io', 'symonyeal.github.io')}.</p>
</div></footer>
</body>
</html>
"""


def figure(p, sizes):
    if "formula" in p:
        return (f'<figure class="fig formula"><div class="eq" role="img" aria-label="{e(p["caption"])}">'
                f'{e(p["formula"])}</div><figcaption>{e(p["caption"])}</figcaption></figure>')
    s = p["slug"]
    return (f'<figure class="fig"><a href="img/{s}-1200.webp" title="Open full size">'
            f'<img src="img/{s}-1200.webp" srcset="img/{s}-600.webp 600w, img/{s}-1200.webp 1200w" '
            f'sizes="{sizes}" width="1200" height="800" loading="lazy" decoding="async" alt="{e(p["image_alt"])}"></a>'
            f'<figcaption>{e(p["caption"])}</figcaption></figure>')


def links(p):
    return '<p class="links">' + "".join(a(u, l, "btn" if i == 0 else "") for i, (l, u) in enumerate(p["links"])) + "</p>"


def writeup(p, results=True):
    """Situation, answer, scope, author; the method on demand."""
    res = "".join(f"<li>{e(r)}</li>" for r in p["results"])
    return f"""<dl class="wu">
<dt>Problem</dt><dd>{e(p['problem'])}</dd>
{f'<dt>Results</dt><dd><ul>{res}</ul></dd>' if results else ''}
<dt>Limits</dt><dd>{e(p['limits'])}</dd>
<dt>Contribution</dt><dd>{e(p['contribution'])}</dd>
</dl>
<details class="method"><summary>Method</summary><p>{e(p['approach'])}</p></details>"""


def meta(p):
    return f'<p class="meta">{e(p["subject"])} · {e(p["year"])}</p>'


def feature(p):
    return f"""<article class="feature" id="{p['slug']}">
{figure(p, "(min-width: 60rem) 34rem, 100vw")}
<div class="body">
{meta(p)}
<h3>{e(p['title'])}</h3>
<p class="headline">{e(p['headline'])}</p>
{writeup(p)}
{links(p)}
</div>
</article>"""


def card(p):
    more = (f'<p><a href="#{p["slug"]}">Full summary above</a></p>' if p.get("featured")
            else f"<details><summary>Problem, results and limits</summary>{writeup(p)}</details>")
    tags = "".join(f"<li>{e(t)}</li>" for t in p["tags"])
    return f"""<li class="card" data-subject="{e(p['subject'])}">
{figure(p, "(min-width: 60rem) 22rem, (min-width: 40rem) 45vw, 100vw")}
{meta(p)}
<h3>{e(p['title'])}</h3>
<p>{e(p['headline'])}</p>
<ul class="tags" aria-label="Methods">{tags}</ul>
{more}
{links(p)}
</li>"""


def index():
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in P["facts"])
    areas = "".join(f"<div><h3>{e(k)}</h3><p>{e(v)}</p></div>" for k, v in P["areas"])
    intro = "".join(f"<p>{e(x)}</p>" for x in P["intro"])
    subj = [s for s in SUBJECTS if any(p["subject"] == s for p in PR)]
    assert all(p["subject"] in SUBJECTS for p in PR), "unknown subject"
    filt = "".join(f'<button type="button" aria-pressed="false" data-subject="{e(s)}">{e(s)}</button>' for s in subj)
    jobs = "".join(f"<li><span class=\"when\">{e(x['dates'])}</span><span><strong>{e(x['title'])}</strong>, {e(x['org'])}</span></li>"
                   for x in CV["experience"])
    eds = "".join(f"<li><span class=\"when\">{e(x['dates'])}</span><span><strong>{e(x['degree'])}</strong>, {e(x['org'])}</span></li>"
                  for x in CV["education"])
    desc = f"{P['name']}: {P['role'].lower()}. {P['lead']}"
    return head(f"{P['name']} · {P['role']}", desc, "") + f"""<main id="main">
<section class="hero wrap{' has-photo' if P['photo'] else ''}" aria-labelledby="name">
{f'<img class="photo" src="{e(P["photo"])}" width="600" height="600" alt="Portrait of {e(P["name"])}">' if P['photo'] else ''}
<h1 id="name">{e(P['name'])}</h1>
<p class="role">{e(P['role'])} · {e(P['location'])}</p>
{f'<p class="status">{e(P["status"])}</p>' if P['status'] else ''}
<p class="lead">{e(P['lead'])}</p>
<div class="intro">{intro}</div>
<dl class="facts">{facts}</dl>
<p class="links">{a('resume.html', 'Résumé', 'btn')}{a(PDF, 'Download PDF')}{a(P['github'], 'GitHub')}{a(P['linkedin'], 'LinkedIn')}{a('mailto:' + P['email'], 'Email')}</p>
</section>

<section class="areas wrap" aria-labelledby="areas-h">
<h2 id="areas-h">What I work on</h2>
<div class="cols">{areas}</div>
</section>

<section id="work" class="wrap" aria-labelledby="work-h">
<h2 id="work-h">Selected work</h2>
<p class="note">Each summary leads with the finding, then states the problem, the method, the results and what the work does not show. Numbers are taken from the project’s repository.</p>
{''.join(feature(p) for p in PR if p.get('featured'))}
</section>

<section id="projects" class="wrap" aria-labelledby="projects-h">
<h2 id="projects-h">All projects</h2>
<div class="filter" role="group" aria-label="Filter by subject" hidden><button type="button" aria-pressed="true" data-subject="">All</button>{filt}</div>
<p class="count" aria-live="polite"></p>
<ul class="grid">{''.join(card(p) for p in PR)}</ul>
</section>

<section id="experience" class="wrap" aria-labelledby="exp-h">
<h2 id="exp-h">Experience</h2>
<ul class="timeline">{jobs}</ul>
<h3>Education</h3>
<ul class="timeline">{eds}</ul>
<p class="links">{a('resume.html', 'Full résumé', 'btn')}{a(PDF, 'Download PDF')}</p>
</section>

<section id="contact" class="wrap" aria-labelledby="contact-h">
<h2 id="contact-h">Contact</h2>
<p>I welcome questions about the projects, research collaboration and roles in operations research or data science.</p>
<ul class="contact">
<li><span>Email</span>{a('mailto:' + P['email'], P['email'])}</li>
<li><span>LinkedIn</span>{a(P['linkedin'], 'linkedin.com/in/saimon-islam-b9291292')}</li>
<li><span>GitHub</span>{a(P['github'], 'github.com/symonyeal')}</li>
</ul>
</section>
</main>
<script src="assets/filter.js" defer></script>
""" + foot()


def resume():
    def job(x):
        note = f'<p class="note">{e(x["note"])}</p>' if "note" in x else ""
        pts = "".join(f"<li>{e(t)}</li>" for t in x["points"])
        return f"""<article class="job"><div class="row"><h3>{e(x['title'])}</h3><span class="when">{e(x['dates'])}</span></div>
<div class="row sub"><span>{e(x['org'])}</span><span>{e(x['place'])}</span></div>{note}<ul>{pts}</ul></article>"""

    def ed(x):
        rows = [f"GPA {e(x['gpa'])}"]
        if "thesis" in x:
            rows.append(f"Thesis: {a(x['thesis_url'], x['thesis'])} (senior supervisor: {e(x['supervisor'])})")
        if "courses" in x:
            rows.append(f"Courses: {e(x['courses'])}")
        rows.append(f"Awards: {e(x['awards'])}")
        return f"""<article class="job"><div class="row"><h3>{e(x['degree'])}</h3><span class="when">{e(x['dates'])}</span></div>
<div class="row sub"><span>{e(x['org'])}</span><span>{e(x['place'])}</span></div><ul class="plain">{''.join(f'<li>{r}</li>' for r in rows)}</ul></article>"""

    skills = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in CV["skills"].items())
    contact = " · ".join([a("mailto:" + P["email"], P["email"]), a(P["linkedin"], "linkedin.com/in/saimon-islam-b9291292"),
                          a(P["github"], "github.com/symonyeal"), a(P["site"], "symonyeal.github.io"),
                          e(P["location"]), e(CV["availability"])])
    return head(f"Résumé · {P['name']}", f"Résumé of {P['name']}: experience, education and skills.", "resume.html") + f"""<main id="main" class="cv wrap">
<div class="cv-head">
<h1>{e(P['name'])}</h1>
<p class="contactline">{contact}</p>
<p class="links noprint">{a(PDF, 'Download PDF', 'btn')}{a('./#work', 'Projects')}</p>
</div>
<section aria-labelledby="sum-h"><h2 id="sum-h">Summary</h2><p>{e(CV['summary'])}</p></section>
<section aria-labelledby="xp-h"><h2 id="xp-h">Experience</h2>{''.join(job(x) for x in CV['experience'])}</section>
<section aria-labelledby="ed-h"><h2 id="ed-h">Education</h2>{''.join(ed(x) for x in CV['education'])}</section>
<section aria-labelledby="sk-h"><h2 id="sk-h">Technical skills</h2><dl class="skills">{skills}</dl></section>
<section class="noprint" aria-labelledby="pj-h"><h2 id="pj-h">Public projects</h2>
<p>Nine research repositories with code, data provenance and stated limits: {a('./#projects', 'see the project gallery')}.</p></section>
</main>
""" + foot()


def og():
    """The 1200×627 link-preview card, rendered by Edge."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="assets/style.css">
<style>body{{margin:0;width:1200px;height:627px;display:grid;grid-template-columns:1fr 560px;align-items:center;background:var(--bg)}}
.t{{padding:0 0 0 72px}}h1{{font-size:66px;margin:0 0 6px}}p{{margin:0 0 22px;max-width:24ch}}
.r{{font:24px var(--sans);color:var(--muted)}}.l{{font-size:31px;line-height:1.35}}.u{{font:20px var(--sans);color:var(--accent)}}
img{{width:520px;border:1px solid var(--rule);border-radius:6px}}</style></head>
<body><div class="t"><h1>{e(P['name'])}</h1><p class="r">{e(P['role'])}</p><p class="l">{e(P['lead'])}</p>
<p class="u">symonyeal.github.io</p></div>
<img src="img/supply-chain-cuts-1200.webp" alt=""></body></html>"""


def render():
    from playwright.sync_api import sync_playwright
    (SITE / "_og.html").write_text(og(), encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 1200, "height": 627}, color_scheme="light")
        pg.goto((SITE / "_og.html").as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=SITE / "og.png")
        pg.goto((SITE / "resume.html").as_uri()); pg.emulate_media(media="print"); pg.wait_for_timeout(300)
        pg.pdf(path=SITE / PDF, format="Letter", print_background=False,
               margin={"top": "0.55in", "bottom": "0.55in", "left": "0.6in", "right": "0.6in"})
        b.close()
    (SITE / "_og.html").unlink()


def pages():
    return {"index.html": index(), "resume.html": resume()}


if __name__ == "__main__":
    for k, v in pages().items():
        (SITE / k).write_text(v, encoding="utf-8", newline="\n")
    if "--render" in sys.argv:
        render()
