---
description: Regenerate the CV .docx from the site content + cv/cv-extra.json
---

Regenerate the CV by running the deterministic generator:

```
python3 cv/generate_cv.py
```

The generator is the single source of truth — do **not** hand-edit the output `.docx`
and do **not** edit the content yourself. Shared sections (summary, experience, skills,
projects, contact) are parsed from `index.html`; Education/Certifications and any contact
overrides come from `cv/cv-extra.json`.

After running:
- Relay the script's summary (counts pulled from `index.html` and `cv/cv-extra.json`, the
  output path and byte size).
- If the script exits with an error, show it verbatim — most likely the page structure
  changed (a parse anchor wasn't found) or `cv/cv-extra.json` has a JSON syntax error.
- Mention that `assets/CV_Mateusz_Filipczak.docx` was overwritten and that, to change
  Education/Certifications, the user edits `cv/cv-extra.json` (not the docx).

Do not commit anything unless the user asks. Do not edit files as part of this command —
just run the generator and report.
