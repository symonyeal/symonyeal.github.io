# Decisions

Each entry: the decision, the alternatives, the reason, the date. Superseded designs are in the git history.

## Design (current)

- **Static pages generated from TOML** (2026-10-20). Alternatives: hand-written HTML (the résumé page
  and PDF drift apart); JSON rendered by JavaScript (content invisible without script, slower first
  paint). `tomllib` is in the standard library, so the build has no dependency.
- **The PDF is printed from `resume.html`.** One source for both; the print stylesheet sets Letter
  size and two pages.
- **One column, white page, Inter, one blue link colour** (2026-10-20, after the owner rejected the
  serif, coloured and plain variants). Inter is OFL, self-hosted as a 48 kB latin subset; no font CDN.
- **Project cards are text in a two-column grid.** Each card says what the project is and what it
  found, in plain first person, with the numbers unchanged from the sources. The write-up fields
  (problem, approach, results, limits) stay in `content/projects.toml` as the source of the headline.
- **Structure follows the pyramid principle.** The introduction states degree, thesis, employment and
  what the projects cover; each project leads with its finding.
- **Projects are listed in `content/projects.toml` order**, twelve at 2026-11-08, each with a `source`
  field naming the README section and revision it was copied from.
- **Card numbers are checked against the origin README** (2026-11-08): `qa/sources.py` lists every
  headline number that the repository README at HEAD does not contain, and every outbound link that
  does not answer 200. It runs in CI. A number that moves in a README fails the check, so the card is
  re-copied.

## Résumé

- **Transcription of the owner's Word master** (2026-10-20). Omitted: phone number. Corrected:
  "aSaimon" → "Saimon"; "PostGRE" → "PostgreSQL"; "SciPy PuLP" → "SciPy, PuLP"; "Excel- VBA" →
  "Excel VBA"; "Sharepoint" → "SharePoint"; "Coordinated in the development" → "Coordinated the
  development"; "evaluates" → "evaluate"; "premier provider" → "principal provider"; "Anesthesia"
  lower-cased mid-sentence; "modeling" → "modelling". Added from the thesis title page: thesis title
  and senior supervisor. Added: Washington and Lee's location (Lexington, VA).
- **Owner's answers** (2026-10-20): no AI-assistance disclosure; the four SFU research-assistant
  percentages (15%, 30%, 25%, 18%) removed, each bullet keeps the work it describes, counts (50+,
  10+, 20+, 15+) unchanged; skills gained JavaScript and an "Optimization and mathematics" line
  (Gurobi, CPLEX, HiGHS, SCIP, Pyomo, SageMath), all evidenced by the résumé bullets or the public
  repositories; LinkedIn URL confirmed. The headshot and status line would come from LinkedIn, which
  refuses automated access, so they are optional fields (`photo`, `status` in `content/profile.toml`)
  awaiting the owner's files.
- **Re-transcribed from the current Word master** (`Saimon Islam Master Original Resume.docx`, which the
  owner rewrote 2026-11-01 to 2026-11-03), 2026-11-07: Government of Yukon role added, Incepta role and
  University of Edinburgh exchange added, SFU research bullets replace the earlier ones, ATA dated
  Dec 2020, summary, skills and courses as in the master. The contact line follows the master's header
  ("No sponsorship required · Willing to relocate"); phone still omitted. The master's Projects and
  activities sections are not transcribed: the projects are on the home page. Education entries may
  omit GPA and awards (the exchange semester has neither).
- **Thesis link** moved to `thesis/2024/deposited.pdf`; the old manuscript path returned 404.

## Project cards, 2026-11-07

- **Rechecked against each repository's README on `main`.** Corrected: Electric Fleet (four certified
  optima; duals come from the simplex LP, not an interior-point master), MMA counts, Renter Cost
  Burden (now the Canadian atlas, not the US county study), Electricity (Dantzig–Wolfe, random-system
  agreement and the archived battery backtest are no longer in the repository), Resilient Supplier
  Panels (branch and bound, 2 µs median, releases link). Language tags follow each repository.
  Added: Minimal Metabolic Interventions, Canada Regional Profiles, Open-Source Watch (crediting
  IRONSIGHT).
- **Agent instruction files** (`CLAUDE.md`, `AGENTS.md`) and local tooling notes removed from the
  published tree.

## Open

See [OPEN.md](OPEN.md).
