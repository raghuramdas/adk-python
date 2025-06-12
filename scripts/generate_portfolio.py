"""Generate an HTML portfolio slide deck.

This script creates an index.html file under ``assets/portfolio`` which
uses the Reveal.js presentation framework. Each slide shows a screenshot
of a site along with a link to the live website. Screenshots are loaded
from an online thumbnail service so no local browser automation is
required.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote_plus

PORTFOLIO_JSON = Path(__file__).with_name("portfolio_sites.json")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "portfolio"

THUMB_URL = "https://image.thum.io/get/width/1280/{url}"


def create_slide(site: dict[str, object]) -> str:
    """Return HTML for a single slide."""
    name = site["name"]
    url = site["url"]
    has_apps = site.get("apps", False)
    screenshot = THUMB_URL.format(url=quote_plus(url))
    apps_text = "<p>Includes mobile apps</p>" if has_apps else ""
    return f"""
<section>
  <h2><a href=\"{url}\">{name}</a></h2>
  <img src=\"{screenshot}\" alt=\"{name} screenshot\" style=\"max-width:90%;height:auto;\">
  {apps_text}
</section>"""


def generate_html(sites: list[dict[str, object]]) -> str:
    slides = [
        "<section><h1>Project Portfolio</h1><p>Web and Mobile Applications</p></section>"
    ]
    for site in sites:
        slides.append(create_slide(site))
    slides_html = "\n".join(slides)
    return f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Portfolio</title>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.2/reveal.min.css'>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.2/theme/black.min.css'>
</head>
<body>
  <div class='reveal'>
    <div class='slides'>
{slides_html}
    </div>
  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.2/reveal.min.js'></script>
  <script>Reveal.initialize();</script>
</body>
</html>"""


def main() -> None:
    sites = json.loads(PORTFOLIO_JSON.read_text())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html = generate_html(sites)
    (OUTPUT_DIR / "index.html").write_text(html)
    print(f"Wrote {OUTPUT_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
