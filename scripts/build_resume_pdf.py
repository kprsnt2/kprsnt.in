"""Regenerate static/Prashanth_Kumar_Kadasi_Resume.pdf from the site's resume data.

The PDF is printed from /resume/print, which renders the same constants as the
/resume page (api/data/projects.py, api/resume_data.py). Edit the data, then run:

    python scripts/build_resume_pdf.py

Needs Chrome or Edge installed (set CHROME_PATH to override the lookup). No
server has to be running: the page is rendered through Flask's test client.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "static" / "Prashanth_Kumar_Kadasi_Resume.pdf"

BROWSER_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]


def find_browser():
    for candidate in BROWSER_CANDIDATES:
        if candidate and os.path.exists(candidate):
            return candidate
    sys.exit("No Chrome/Edge found. Set CHROME_PATH to the browser executable.")


def render_html():
    sys.path.insert(0, str(ROOT))
    from api.index import app

    response = app.test_client().get("/resume/print")
    if response.status_code != 200:
        sys.exit(f"/resume/print returned {response.status_code}")
    return response.get_data(as_text=True)


def main():
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "resume.html"
        html_path.write_text(render_html(), encoding="utf-8")
        out_path = Path(tmp) / "resume.pdf"
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                f"--user-data-dir={Path(tmp) / 'profile'}",
                "--no-pdf-header-footer",
                f"--print-to-pdf={out_path}",
                html_path.as_uri(),
            ],
            check=True,
            timeout=120,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if not out_path.exists() or out_path.stat().st_size < 1000:
            sys.exit("Browser did not produce a PDF.")
        shutil.copyfile(out_path, PDF_PATH)
    pages = PDF_PATH.read_bytes().count(b"/Type /Page") - PDF_PATH.read_bytes().count(b"/Type /Pages")
    print(f"Wrote {PDF_PATH} ({PDF_PATH.stat().st_size // 1024} KB, {pages} pages)")


if __name__ == "__main__":
    main()
