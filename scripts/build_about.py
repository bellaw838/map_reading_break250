#!/usr/bin/env python3
"""Regenerate about.html from about.md.

Usage: python3 scripts/build_about.py

Supported markdown: `# Heading` (page title), plain paragraphs, **bold**,
and a whole paragraph wrapped in *...* (rendered as the italic closing note,
styled like the wordbank about page's thanks line).
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "about.md"
OUT = ROOT / "about.html"


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def main():
    blocks = [b.strip() for b in SRC.read_text().split("\n\n") if b.strip()]

    title = "About"
    body = []
    for block in blocks:
        flat = " ".join(line.strip() for line in block.splitlines())
        if flat.startswith("# "):
            title = flat[2:].strip()
        elif flat.startswith("*") and flat.endswith("*") and not flat.startswith("**"):
            body.append(
                '      <p class="pt-6 border-t border-slate-200 text-base '
                'text-slate-500 italic">%s</p>' % inline(flat[1:-1])
            )
        else:
            body.append("      <p>%s</p>" % inline(flat))

    page = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>%(title)s — Break MAP Reading 250+</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%%22http://www.w3.org/2000/svg%%22 viewBox=%%220 0 100 100%%22><text y=%%22.9em%%22 font-size=%%2290%%22>📖</text></svg>" />
</head>
<body class="min-h-screen bg-slate-50 text-slate-800">
  <main class="max-w-2xl mx-auto px-6 py-10 md:py-16 space-y-8">
    <a href="./" class="inline-flex items-center text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
      <span aria-hidden="true" class="mr-2">&larr;</span> Back to home
    </a>

    <h1 class="text-4xl font-bold tracking-tight text-slate-900">%(title)s</h1>

    <div class="text-lg text-slate-700 leading-relaxed font-serif space-y-6">
%(body)s
    </div>
  </main>
</body>
</html>
""" % {"title": html.escape(title), "body": "\n".join(body)}

    OUT.write_text(page)
    print("Wrote %s (%d paragraphs)" % (OUT.relative_to(ROOT), len(body)))


if __name__ == "__main__":
    main()
