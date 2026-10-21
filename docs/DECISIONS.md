# Decisions

Each entry: the decision, the alternatives, the reason, the date.

## 2026-10-20

- **Static pages generated from TOML.** Alternatives: hand-written HTML (the résumé page and PDF
  drift apart); JSON rendered by JavaScript (content invisible without script, slower first
  paint). `tomllib` is in the standard library, so the build has no dependency.
- **The PDF is printed from `resume.html`.** One source for both; the print stylesheet sets
  Letter size and two pages.
- **Structure follows the pyramid principle.** The hero states the governing thought, then three
  supporting facts. Each project leads with its finding, then problem, results, limits and
  contribution; the method is one click away. Subjects are mutually exclusive, so the filter
  partitions the gallery.
- **Five selected projects.** Electric fleet, supply-chain cuts and supplier panels show the
  certificate-carrying optimization work; the thesis serves research readers; MMA rankings is
  the most developed site. All nine appear in the gallery.
- **Figures** were captured from the live sites on 2026-10-20 (Edge, 1440 px, light scheme) or
  taken from repository figures, cropped to 3:2 and padded with their own background where
  narrower. The sparse-portfolio project has no figure, so its model is shown as a formula.
- **Self-hosted Source Serif 4**, latin subset, two variable files (250 kB). No font CDN.
- **Résumé transcription changes.** Omitted: phone number, work-permit line. Corrected: "aSaimon"
  → "Saimon"; "PostGRE" → "PostgreSQL"; "SciPy PuLP" → "SciPy, PuLP"; "Excel- VBA" → "Excel VBA";
  "Sharepoint" → "SharePoint"; "Coordinated in the development" → "Coordinated the development";
  "evaluates" → "evaluate"; "premier provider" → "principal provider"; "Anesthesia" lower-cased
  mid-sentence; "modeling" → "modelling". Added from the thesis title page: thesis title and
  senior supervisor. Added: Washington and Lee's location (Lexington, VA).

## 2026-10-20, owner's answers

- Ministry bullet corrected from 80% to 20%, agreeing with the summary.
- "On valid work permit" shown in the résumé contact line and PDF. Phone stays omitted.
- No AI-assistance disclosure.
- The four SFU research-assistant percentages (15%, 30%, 25%, 18%) removed; each bullet keeps
  the work it describes. Counts (50+, 10+, 20+, 15+) unchanged.
- Skills: JavaScript added; new line "Optimization and mathematics": Gurobi, CPLEX, HiGHS, SCIP,
  Pyomo, SageMath (all evidenced by the résumé bullets or the public repositories).
- Headshot and status line come from LinkedIn; LinkedIn refuses automated access, so they are
  optional fields (`photo`, `status` in `content/profile.toml`) awaiting the owner's files.
- LinkedIn URL confirmed by the owner.

## Open

See [OPEN.md](OPEN.md).
