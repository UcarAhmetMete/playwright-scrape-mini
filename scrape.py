import argparse
import json
import logging
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def scrape(url: str, outdir: Path, headless: bool, timeout: int) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    out_file = outdir / "scrape.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            title = page.title()

            h1 = None
            h1_locator = page.locator("h1").first
            try:
                if h1_locator.count() > 0:
                    h1 = h1_locator.inner_text()
            except Exception:
                logging.debug("Could not read h1 text", exc_info=True)

            links = page.locator("a").count()

        except Exception:
            logging.exception("Failed to scrape %s", url)
            browser.close()
            raise

        finally:
            try:
                browser.close()
            except Exception:
                pass

    data = {"url": url, "title": title, "h1": h1, "link_count": links}
    out_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Tiny Playwright scraper")
    parser.add_argument("--url", default="https://example.com", help="URL to scrape")
    parser.add_argument("--out", default="out", help="Output directory")
    parser.add_argument("--no-headless", action="store_true", help="Run browser headed")
    parser.add_argument("--timeout", type=int, default=30000, help="Navigation timeout in ms")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")

    headless = not args.no_headless
    outdir = Path(args.out)

    try:
        out_file = scrape(args.url, outdir, headless, args.timeout)
        print(f"Wrote {out_file}")
    except Exception:
        logging.error("Scrape failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
