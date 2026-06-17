#!/usr/bin/env python3
"""
Deterministic CV generator.

Builds assets/CV_Mateusz_Filipczak.docx from:
  - index.html      (shared content: summary, experience, skills, projects, contact)
  - cv/cv-extra.json (CV-only content: education, certifications, + optional overrides)

Pure Python standard library only — no third-party deps, no network, no clock/RNG —
so the same inputs always produce a byte-for-byte identical .docx.

Run:  python3 cv/generate_cv.py
"""

import html
import json
import os
import re
import struct
import sys
import zipfile
import zlib
from html.parser import HTMLParser

# ── paths ───────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(ROOT, "index.html")
EXTRA_JSON = os.path.join(ROOT, "cv", "cv-extra.json")
OUT_DOCX = os.path.join(ROOT, "assets", "CV_Mateusz_Filipczak.docx")

# ── styling constants (match the site) ───────────────────────────────────────
ACCENT = "8C6EDC"
TEXT = "1A1A1A"
MUTED = "6E6E6E"
FONT = "Segoe UI"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ── minimal HTML tree ────────────────────────────────────────────────────────
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag=None, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []
        self.parent = None

    def has_class(self, c):
        return c in self.attrs.get("class", "").split()

    def text(self):
        out = []
        for ch in self.children:
            out.append(ch if isinstance(ch, str) else ch.text())
        return "".join(out)

    def find_all(self, tag=None, cls=None):
        res = []
        for ch in self.children:
            if isinstance(ch, Node):
                if (tag is None or ch.tag == tag) and (cls is None or ch.has_class(cls)):
                    res.append(ch)
                res.extend(ch.find_all(tag, cls))
        return res

    def find(self, tag=None, cls=None):
        r = self.find_all(tag, cls)
        return r[0] if r else None


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs)
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_tree(text):
    tb = TreeBuilder()
    tb.feed(text)
    return tb.root


def need(value, what):
    if not value:
        raise SystemExit(f"[generate_cv] could not find {what} in index.html — "
                         f"did the page structure change?")
    return value


# ── stage 1: parse index.html ────────────────────────────────────────────────
def extract_page(text):
    root = parse_tree(text)
    d = {}

    d["name"] = clean(need(root.find(cls="home-name"), "name (.home-name)").text())
    d["headline"] = clean(need(root.find(cls="home-tagline"), "headline (.home-tagline)").text())
    d["summary"] = clean(need(root.find(cls="about-text"), "summary (.about-text)").text())

    # experience
    d["experience"] = []
    for entry in need(root.find_all(cls="exp-entry"), "experience (.exp-entry)"):
        e = {
            "title": clean(_textof(entry, "exp-title")),
            "date": clean(_textof(entry, "exp-date")),
            "company": clean(_textof(entry, "exp-company")),
            "promo": None,
            "bullets": [],
            "projects": [],
        }
        promo = entry.find(cls="exp-promo")
        if promo:
            e["promo"] = clean(promo.text())
        proj_wrap = entry.find(cls="exp-projects")
        if proj_wrap:
            for proj in proj_wrap.find_all(cls="exp-project"):
                ul = proj.find(cls="exp-bullets")
                e["projects"].append({
                    "name": clean(_textof(proj, "exp-project-name")),
                    "bullets": [clean(li.text()) for li in ul.find_all("li")] if ul else [],
                })
        else:
            ul = entry.find(cls="exp-bullets")
            if ul:
                e["bullets"] = [clean(li.text()) for li in ul.find_all("li")]
        d["experience"].append(e)

    # skills
    d["skills"] = []
    for cat in need(root.find_all(cls="skill-category"), "skills (.skill-category)"):
        h3 = cat.find("h3")
        level_node = h3.find(cls="skill-level") if h3 else None
        level = clean(level_node.text()) if level_node else ""
        full = clean(h3.text()) if h3 else ""
        name = clean(full[: len(full) - len(level)]) if level and full.endswith(level) else full
        d["skills"].append({
            "category": name,
            "level": level,
            "tags": [clean(t.text()) for t in cat.find_all(cls="skill-tag")],
        })

    # projects
    d["projects"] = []
    for card in root.find_all(cls="project-card"):
        h3 = card.find("h3")
        p = card.find("p")
        d["projects"].append({
            "name": clean(h3.text()) if h3 else "",
            "description": clean(p.text()) if p else "",
        })

    # contact (best-effort; overridable from cv-extra.json)
    contact = {}
    btn = root.find(cls="contact-btn")
    if btn and btn.attrs.get("href", "").startswith("mailto:"):
        contact["email"] = btn.attrs["href"][len("mailto:"):]
    for row in root.find_all(cls="contact-row"):
        a = row.find("a")
        if a and a.attrs.get("href", "").startswith("http"):
            contact["website"] = clean(a.text())
        else:
            span = row.find("span")
            if span:
                contact["location"] = clean(span.text())
    d["contact"] = contact
    return d


def _textof(node, cls):
    n = node.find(cls=cls)
    return n.text() if n else ""


# ── stage 2: load cv-extra.json ──────────────────────────────────────────────
DEFAULT_OPTIONS = {
    "include_projects": True,
    "section_order": ["summary", "experience", "projects", "skills",
                      "education", "certifications"],
}


def load_extra(path):
    if not os.path.exists(path):
        raise SystemExit(f"[generate_cv] missing {path}")
    with open(path, encoding="utf-8") as f:
        extra = json.load(f)
    extra.setdefault("education", [])
    extra.setdefault("certifications", [])
    extra.setdefault("contact", {})
    opts = dict(DEFAULT_OPTIONS)
    opts.update(extra.get("options", {}))
    extra["options"] = opts
    return extra


# ── stage 3: DOCX (OOXML) builder ────────────────────────────────────────────
def esc(s):
    return html.escape(s, quote=True)


def rpr(bold=False, italic=False, size=None, color=None):
    p = "<w:rPr>"
    p += f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
    if bold:
        p += "<w:b/>"
    if italic:
        p += "<w:i/>"
    if color:
        p += f'<w:color w:val="{color}"/>'
    if size:
        p += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    p += "</w:rPr>"
    return p


def run(text, **kw):
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def para(runs, before=0, after=80, line=None, indent=None, hanging=None,
         border=False, align=None):
    if isinstance(runs, str):
        runs = [runs]
    pPr = "<w:pPr>"
    if border:
        pPr += ('<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="3" '
                'w:color="D9D9D9"/></w:pBdr>')
    sp = f'<w:spacing w:before="{before}" w:after="{after}"'
    if line:
        sp += f' w:line="{line}" w:lineRule="auto"'
    sp += "/>"
    pPr += sp
    if indent is not None or hanging is not None:
        pPr += "<w:ind"
        if indent is not None:
            pPr += f' w:left="{indent}"'
        if hanging is not None:
            pPr += f' w:hanging="{hanging}"'
        pPr += "/>"
    if align:
        pPr += f'<w:jc w:val="{align}"/>'
    pPr += "</w:pPr>"
    return f"<w:p>{pPr}{''.join(runs)}</w:p>"


def heading(text):
    return para([run(text.upper(), bold=True, size=24, color=ACCENT)],
                before=260, after=120, border=True)


def bullet(text):
    return para([run("•", color=ACCENT), run("\t" + text, size=19)],
                after=40, indent=288, hanging=288)


def build_body(model):
    b = []
    # header
    b.append(para([run(model["name"], bold=True, size=44, color=TEXT)], after=20))
    b.append(para([run(model["headline"], size=24, color=ACCENT)], after=20))
    contact = model["contact"]
    bits = [contact.get(k) for k in ("email", "website", "location") if contact.get(k)]
    if contact.get("phone"):
        bits.insert(0, contact["phone"])
    if contact.get("linkedin"):
        bits.append(contact["linkedin"])
    if bits:
        runs = []
        for i, t in enumerate(bits):
            if i:
                runs.append(run("   ·   ", size=18, color=ACCENT))
            runs.append(run(t, size=18, color=MUTED))
        b.append(para(runs, after=80))

    def summary():
        if model.get("summary"):
            b.append(heading("Summary"))
            b.append(para([run(model["summary"], size=19)], after=100, line=276))

    def experience():
        if not model.get("experience"):
            return
        b.append(heading("Experience"))
        for e in model["experience"]:
            b.append(para([run(e["title"], bold=True, size=21, color=TEXT)],
                          before=140, after=10))
            meta = [run(e["company"], size=18, color=ACCENT)]
            if e.get("date"):
                meta.append(run("    ·    " + e["date"], size=18, color=MUTED))
            b.append(para(meta, after=20))
            if e.get("promo"):
                b.append(para([run(e["promo"], italic=True, size=17, color=MUTED)], after=40))
            for bl in e.get("bullets", []):
                b.append(bullet(bl))
            for proj in e.get("projects", []):
                b.append(para([run(proj["name"], bold=True, size=18, color=TEXT)],
                              before=60, after=20))
                for bl in proj["bullets"]:
                    b.append(bullet(bl))

    def projects():
        if not (model["options"]["include_projects"] and model.get("projects")):
            return
        b.append(heading("Projects"))
        for p in model["projects"]:
            b.append(para([run(p["name"], bold=True, size=20, color=TEXT)],
                          before=70, after=10))
            if p.get("description"):
                b.append(para([run(p["description"], size=19, color=MUTED)], after=40))

    def skills():
        if not model.get("skills"):
            return
        b.append(heading("Skills"))
        for s in model["skills"]:
            line = [run(s["category"], bold=True, size=19, color=TEXT)]
            if s.get("level"):
                line.append(run("   " + s["level"], italic=True, size=17, color=ACCENT))
            b.append(para(line, before=70, after=10))
            if s.get("tags"):
                b.append(para([run(", ".join(s["tags"]), size=18, color=MUTED)], after=40))

    def education():
        items = model.get("education", [])
        if not any(any(v for v in it.values()) for it in items):
            return
        b.append(heading("Education"))
        for it in items:
            if it.get("degree"):
                b.append(para([run(it["degree"], bold=True, size=21, color=TEXT)],
                              before=60, after=10))
            meta = []
            if it.get("institution"):
                meta.append(run(it["institution"], size=18, color=ACCENT))
            if it.get("period"):
                meta.append(run(("    ·    " if meta else "") + it["period"],
                                size=18, color=MUTED))
            if meta:
                b.append(para(meta, after=20 if it.get("details") else 40))
            for det in it.get("details", []):
                b.append(bullet(det))

    def certifications():
        items = model.get("certifications", [])
        rendered = []
        for c in items:
            label = c.get("name", "")
            tail = ", ".join(x for x in (c.get("issuer"), c.get("year")) if x)
            if tail:
                label = f"{label} — {tail}" if label else tail
            if label.strip():
                rendered.append(label)
        if not rendered:
            return
        b.append(heading("Certifications"))
        for label in rendered:
            b.append(bullet(label))

    sections = {
        "summary": summary, "experience": experience, "projects": projects,
        "skills": skills, "education": education, "certifications": certifications,
    }
    for key in model["options"]["section_order"]:
        fn = sections.get(key)
        if fn:
            fn()
    return b


def build_docx_bytes(model):
    body = build_body(model)
    sectPr = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
              '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
              'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>" + "".join(body) + sectPr + "</w:body></w:document>")

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
        f'<w:color w:val="{TEXT}"/><w:sz w:val="20"/><w:szCs w:val="20"/>'
        "</w:rPr></w:rPrDefault></w:docDefaults>"
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/></w:style></w:styles>')

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        "</Types>")

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>")

    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>")

    # fixed order + fixed timestamp => byte-identical output
    parts = [
        ("[Content_Types].xml", content_types),
        ("_rels/.rels", rels),
        ("word/document.xml", document_xml),
        ("word/styles.xml", styles_xml),
        ("word/_rels/document.xml.rels", doc_rels),
    ]
    buf = __import__("io").BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data.encode("utf-8"))
    return buf.getvalue()


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    with open(INDEX_HTML, encoding="utf-8") as f:
        page = extract_page(f.read())
    extra = load_extra(EXTRA_JSON)

    contact = dict(page.get("contact", {}))
    contact.update({k: v for k, v in extra.get("contact", {}).items() if v})

    model = {
        "name": page["name"],
        "headline": page["headline"],
        "summary": page["summary"],
        "experience": page["experience"],
        "skills": page["skills"],
        "projects": page["projects"],
        "contact": contact,
        "education": extra["education"],
        "certifications": extra["certifications"],
        "options": extra["options"],
    }

    data = build_docx_bytes(model)
    os.makedirs(os.path.dirname(OUT_DOCX), exist_ok=True)
    with open(OUT_DOCX, "wb") as f:
        f.write(data)

    # summary for the caller
    rel = os.path.relpath(OUT_DOCX, ROOT)
    print(f"[generate_cv] wrote {rel} ({len(data)} bytes)")
    print(f"  from index.html : {len(model['experience'])} experience, "
          f"{len(model['skills'])} skill groups, {len(model['projects'])} projects")
    print(f"  from cv-extra   : {len(model['education'])} education, "
          f"{len(model['certifications'])} certifications"
          + ("" if model["options"]["include_projects"] else "  (projects excluded)"))


if __name__ == "__main__":
    main()
