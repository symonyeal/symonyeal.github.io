# Working contract

Read before changing anything. [README](README.md) states how the site is built;
[Decisions](docs/DECISIONS.md) why; [Validation](docs/VALIDATION.md) what is checked;
[Open](docs/OPEN.md) what awaits the owner. Codex reads this file through [AGENTS.md](AGENTS.md).

## Always on

| Rule | Reason |
| --- | --- |
| Every claim about a project is copied from that project's README or site, and its entry names the source. | The site is evidence for recruiters and researchers; an invented or rounded-up result is a misstatement. |
| Résumé text changes only when the owner changes the résumé. Typo fixes are listed in Decisions. | The site must agree with the document the owner sends. |
| No phone number or street address on the site or in the PDF. The work-permit line stays (owner's decision, 2026-10-20). | Public page; the owner asked to omit private details. |
| No AI-assistance disclosure in contribution lines. | Owner's decision, 2026-10-20. |
| Content lives in `content/*.toml` only; the HTML and PDF are generated. | One source, so the page, the PDF and the tests cannot disagree. |
| No framework, build tool, CDN or tracker. | Static hosting, fast on a phone, nothing third-party. |
| Figures show the actual work (a result, a solution, a screen), never stock imagery. | The owner's instruction. |
| A change is pushed to `main` once the gate passes; `pages.yml` publishes it. | Published 2026-10-20 with the owner's approval. |

## Before a change is finished

```text
python build.py --render
python -m pytest -q
python -m ruff check .
python qa/browser.py --external
```
