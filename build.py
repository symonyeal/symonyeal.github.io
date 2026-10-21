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
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top wrap">
<a class="brand" href="./">{e(P['name'])}</a>
<nav aria-label="Main"><a href="./#projects">Projects</a> <a href="./#experience">Experience</a> <a href="resume.html">Résumé</a></nav>
</header>
"""


def foot():
    return f"""<footer class="foot wrap">
<p>{a('mailto:' + P['email'], P['email'])} · {a(P['github'], 'GitHub')} · {a(P['linkedin'], 'LinkedIn')} · {a(P['github'] + '/symonyeal.github.io', 'Source')}</p>
</footer>
</body>
</html>
"""


def project(p):
    """Card: title, year and subject, what it is and found, links. The full write-up stays in content/ and the repository."""
    links = "".join(a(u, l) for l, u in p["links"])
    return f"""<li class="card" id="{p['slug']}">
<p class="meta">{e(p['subject'])} · {e(p['year'])}</p>
<h3>{a(p['links'][0][1], p['title'])}</h3>
<p>{e(p['headline'])}</p>
<p class="links">{links}</p>
</li>"""


def index():
    assert all(p["subject"] in SUBJECTS for p in PR), "unknown subject"
    when = lambda x, k: (f"<li><span class=\"when\">{e(x['dates'])}</span>"
                         f"<span>{e(x[k])}, {e(x['org'])}</span></li>")
    jobs = "".join(when(x, "title") for x in CV["experience"])
    eds = "".join(when(x, "degree") for x in CV["education"])
    intro = "".join(f"<p>{e(x)}</p>" for x in P["intro"])
    desc = f"{P['name']}: {P['role'].lower()}, {P['location']}. Projects, experience and résumé."
    return head(f"{P['name']}", desc, "") + f"""<main id="main" class="wrap">
<section class="intro" aria-labelledby="name">
{f'<img class="photo" src="{e(P["photo"])}" width="600" height="600" alt="Portrait of {e(P["name"])}">' if P['photo'] else ''}
<h1 id="name">{e(P['name'])}</h1>
<p class="role">{e(P['role'])} · {e(P['location'])}</p>
{f'<p class="status">{e(P["status"])}</p>' if P['status'] else ''}
{intro}
<p class="links">{a('resume.html', 'Résumé', 'btn')}{a('mailto:' + P['email'], 'Email')}{a(P['github'], 'GitHub')}{a(P['linkedin'], 'LinkedIn')}</p>
</section>

<section id="projects" aria-labelledby="projects-h">
<h2 id="projects-h">Projects</h2>
<ul class="grid">{''.join(project(p) for p in PR)}</ul>
</section>

<section id="experience" aria-labelledby="exp-h">
<h2 id="exp-h">Experience</h2>
<ul class="cvlist">{jobs}</ul>
<h2>Education</h2>
<ul class="cvlist">{eds}</ul>
<p class="links">{a('resume.html', 'Full résumé')}{a(PDF, 'PDF')}</p>
</section>
</main>
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
<p class="links noprint">{a(PDF, 'Download PDF', 'btn')}{a('./#projects', 'Projects')}</p>
</div>
<section aria-labelledby="sum-h"><h2 id="sum-h">Summary</h2><p>{e(CV['summary'])}</p></section>
<section aria-labelledby="xp-h"><h2 id="xp-h">Experience</h2>{''.join(job(x) for x in CV['experience'])}</section>
<section aria-labelledby="ed-h"><h2 id="ed-h">Education</h2>{''.join(ed(x) for x in CV['education'])}</section>
<section aria-labelledby="sk-h"><h2 id="sk-h">Technical skills</h2><dl class="skills">{skills}</dl></section>
<section class="noprint" aria-labelledby="pj-h"><h2 id="pj-h">Public projects</h2>
<p>{len(PR)} projects with code and data: {a('./#projects', 'see the list')}.</p></section>
</main>
""" + foot()


def og():
    """The 1200×627 link-preview card, rendered by Edge."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="assets/style.css">
<style>body{{margin:0;width:1200px;height:627px;display:flex;flex-direction:column;justify-content:center;padding:0 96px;box-sizing:border-box}}
h1{{font-size:84px;margin:0 0 16px}}p{{font-size:34px;margin:0 0 12px;color:var(--muted)}}</style></head>
<body><h1>{e(P['name'])}</h1><p>{e(P['role'])} · {e(P['location'])}</p><p>symonyeal.github.io</p></body></html>"""


def render():
    from playwright.sync_api import sync_playwright
    (SITE / "_og.html").write_text(og(), encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 1200, "height": 627}, color_scheme="light", reduced_motion="reduce")
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
