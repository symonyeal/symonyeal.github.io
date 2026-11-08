# Validation

| Claim | Check | Status |
| --- | --- | --- |
| Pages equal the build of the content | `tests/test_site.py::test_pages_are_built_from_content` | pass 2026-11-08 |
| Every local link and fragment resolves | `test_local_links_resolve` | pass 2026-11-08 |
| Every project has an `https` link, a subject and a repository link | `test_every_project_is_complete` | pass 2026-11-08 |
| No phone number in pages or PDF | `test_no_private_contact_detail` | pass 2026-11-08 |
| PDF has at most two pages and contains every title, organization, date and bullet | `test_pdf_transcribes_resume` | pass 2026-11-08 |
| A card number absent from its README is listed | `test_stale_card_number_is_listed` | pass 2026-11-08 |
| Card numbers appear in each origin README | `qa/sources.py --cards` (CI) | pass 2026-11-08, 12 of 12 cards |
| Outbound links return 200 | `qa/sources.py --links` (CI) | pass 2026-11-08; LinkedIn is skipped (it answers 999 to scripts) and was confirmed by the owner |
| No horizontal scroll at 360, 390, 768, 1440 px; navigation targets exist; PDF served as `application/pdf` | `qa/browser.py` (local, Edge) | not rerun 2026-11-08 |
| Project numbers match their sources | `qa/sources.py` and each entry's `source` field | numbers only; wording is read by hand |
