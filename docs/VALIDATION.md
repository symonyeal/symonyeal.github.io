# Validation

| Claim | Check | Status |
| --- | --- | --- |
| Pages equal the build of the content | `tests/test_site.py::test_pages_are_built_from_content` | pass 2026-10-20 |
| Every local link and fragment resolves | `test_local_links_resolve` | pass 2026-10-20 |
| Every project has a repository link and a figure or formula | `test_every_project_is_complete` | pass 2026-10-20 |
| No phone number in pages or PDF | `test_no_private_contact_detail` | pass 2026-10-20 |
| PDF has at most two pages and contains every title, organization, date and bullet | `test_pdf_transcribes_resume` | pass 2026-10-20 |
| No horizontal scroll at 360, 390, 768, 1440 px, light and dark | `qa/browser.py` | pass 2026-10-20 |
| Navigation targets exist; filter shows exactly each subject's cards; PDF served as `application/pdf` | `qa/browser.py` | pass 2026-10-20 |
| Outbound links return 200 | `qa/browser.py --external` | pass 2026-10-20, except this repository (not yet created) and LinkedIn (needs a browser session) |
| Project numbers match their sources | read against each README on 2026-10-20 | by hand; each entry's `source` field |
