# Saimon Islam

Personal site with research projects, experience and a résumé with a PDF copy.

[Site](https://symonyeal.github.io/)

`build.py` generates static HTML and CSS pages from three TOML content files. The published
site makes no third-party requests and requires no application server.

| Path | Contents |
| --- | --- |
| `content/profile.toml` | Name, introduction, contact links |
| `content/projects.toml` | One entry per project; field meanings at the top of the file |
| `content/resume.toml` | The résumé |
| `build.py` | content → `site/index.html`, `site/resume.html`; `--render` also writes the PDF and `site/og.png` |
| `site/` | The published folder; `*.html`, the PDF and `og.png` are generated, commit them |
| `tests/` | Pages match the content; local links resolve; no phone number; the PDF transcribes the résumé |
| `qa/sources.py` | Card numbers must appear in the origin README; outbound links answer 200 (CI) |
| `qa/browser.py` | Edge checks: no horizontal scroll at 360–1440 px, navigation, PDF download, outbound links |

## Local preview

```text
python build.py
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8765/. Opening `site/index.html` directly also works.

## Project entries

1. Add a `[[project]]` block to `content/projects.toml`. Copy numbers only from the project's
   own README or site.
2. `python build.py`, then the gate below.

## Résumé

Edit `content/resume.toml`, then `python build.py --render` (needs Microsoft Edge and
`pip install playwright`) to regenerate the pages and `site/Saimon-Islam-Resume.pdf`.
The PDF must stay at two pages; a test enforces it.

## Checks

```text
python -m pytest -q
python -m ruff check .
python qa/sources.py                # card numbers against origin READMEs, outbound links
python qa/browser.py                 # with the local server running
```

GitHub Actions runs the first three on every push; `pages.yml` publishes `site/`.

Code: MIT. Text and résumé: © Saimon Islam. Font (Inter): SIL Open Font License (`site/assets/fonts/OFL.txt`).
