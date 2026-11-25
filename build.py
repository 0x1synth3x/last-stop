#!/usr/bin/env python3
"""Build the static GitHub Pages site with commit-specific asset URLs."""

from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "_site"
PLACEHOLDER = "__BUILD_VERSION__"
ASSETS = ("styles.css", "script.js", "stop.svg", "service-worker.js")


class StructureValidator(HTMLParser):
    VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            raise ValueError(f"Unbalanced HTML closing tag: </{tag}>")
        self.stack.pop()

    def finish(self):
        if self.stack:
            raise ValueError(f"Unclosed HTML tags: {', '.join(self.stack)}")


def build(version):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", version):
        raise ValueError("Build version contains unsupported characters")

    source_html = (ROOT / "index.html").read_text(encoding="utf-8")
    if source_html.count(PLACEHOLDER) != 2:
        raise ValueError("index.html must contain exactly two build version placeholders")

    OUTPUT.mkdir(exist_ok=True)
    for old_file in OUTPUT.iterdir():
        if old_file.is_dir():
            shutil.rmtree(old_file)
        else:
            old_file.unlink()

    generated_html = source_html.replace(PLACEHOLDER, version)
    parser = StructureValidator()
    parser.feed(generated_html)
    parser.close()
    parser.finish()
    if PLACEHOLDER in generated_html:
        raise ValueError("Generated HTML still contains a build version placeholder")

    (OUTPUT / "index.html").write_text(generated_html, encoding="utf-8")
    for asset in ASSETS:
        shutil.copy2(ROOT / asset, OUTPUT / asset)

    for element, attribute, expected in (("link", "href", "styles.css"), ("script", "src", "script.js")):
        match = re.search(rf"<{element}\b[^>]*\b{attribute}=\"([^\"]+)\"", generated_html)
        if not match:
            raise ValueError(f"Generated HTML is missing a {expected} reference")
        url = urlsplit(match.group(1))
        asset_path = url.path.removeprefix("./")
        if asset_path != expected or url.query != f"v={version}":
            raise ValueError(f"Invalid generated path or version for {expected}: {match.group(1)}")
        if not (OUTPUT / asset_path).is_file():
            raise ValueError(f"Asset is missing from deployment output: {asset_path}")

    print(f"Built _site for {version}; HTML structure and CSS/JavaScript asset paths are valid.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 build.py <commit-sha>")
    try:
        build(sys.argv[1])
    except (OSError, ValueError) as error:
        raise SystemExit(f"Build failed: {error}") from error
