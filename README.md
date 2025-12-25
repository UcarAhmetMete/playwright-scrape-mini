# Playwright Scrape Mini

Tiny Playwright example that opens a page headless and writes scraped fields to **JSON**.

## Install

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
python scrape.py
```

## Usage

Run the script with optional arguments:

```bash
# default
python scrape.py

# specify url and output dir
python scrape.py --url https://example.com --out my_out

# run headed browser (useful for debugging)
python scrape.py --no-headless --verbose
```

The script writes a `scrape.json` file with keys: `url`, `title`, `h1`, and `link_count`.
