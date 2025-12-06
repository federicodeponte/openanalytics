"""
Local HTML to PDF using Playwright (no external service needed).

Usage:
  python render_pdf.py path/to/report.html --output report.pdf
"""

import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def render_pdf(input_html: str, output_pdf: str) -> None:
    html_path = Path(input_html).resolve()
    output_path = Path(output_pdf).resolve()

    if not html_path.exists():
        raise FileNotFoundError(f"HTML not found: {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(path=str(output_path), format="A4", print_background=True)
        browser.close()
    size_kb = output_path.stat().st_size / 1024
    print(f"✅ PDF saved to {output_path} ({size_kb:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render local HTML to PDF (Playwright)")
    parser.add_argument("html_path", help="Path to HTML file")
    parser.add_argument(
        "--output", "-o", default="report.pdf", help="Output PDF path (default: report.pdf)"
    )
    args = parser.parse_args()
    render_pdf(args.html_path, args.output)


if __name__ == "__main__":
    main()

