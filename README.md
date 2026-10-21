# symonyeal.github.io

Personal site of Saimon Islam: introduction, every public project, experience, and the
full résumé with a PDF. **Site: https://symonyeal.github.io/**.

Static HTML and CSS; no framework, no server, no third-party requests.
Three content files are the single source; `build.py` writes the pages from them.

| Path | Contents |
| --- | --- |
| `content/profile.toml` | Name, introduction, contact links |
| `content/projects.toml` | One entry per project; field meanings at the top of the file |
| `content/resume.toml` | The résumé |
| `build.py` | content → `site/index.html`, `site/resume.html`; `--render` also writes the PDF and `site/og.png` |
| `site/` | The published folder; `*.html`, the PDF and `og.png` are generated, commit them |
| `tests/` | Pages match the content; local links resolve; no phone number; the PDF transcribes the résumé |
| `qa/browser.py` | Edge checks: no horizontal scroll at 360–1440 px, navigation, PDF download, outbound links |

## View locally

```text
python build.py
python -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8765/. Opening `site/index.html` directly also works.

## Add a project

1. Add a `[[project]]` block to `content/projects.toml`. Copy numbers only from the project's
   own README or site.
2. `python build.py`, then the gate below.

## Update the résumé

Edit `content/resume.toml`, then `python build.py --render` (needs Microsoft Edge and
`pip install playwright`) to regenerate the pages and `site/Saimon-Islam-Resume.pdf`.
The PDF must stay at two pages; a test enforces it.

## Gate

```text
python -m pytest -q
python -m ruff check .
python qa/browser.py --external      # with the local server running
```

GitHub Actions runs the first two on every push; `pages.yml` publishes `site/`.

Code: MIT. Text and résumé: © Saimon Islam. Font (Inter): SIL Open Font License (`site/assets/fonts/OFL.txt`).
