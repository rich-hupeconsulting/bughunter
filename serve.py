# serve.py
print("[+] Starting FastAPI app")

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import json
import threading

from modules import recon
from modules.utils import load_scan_log, append_scan_log, update_scan_status

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret123")
app.mount("/static", StaticFiles(directory="static"), name="static")

SCAN_LOG_PATH = Path("data/scan_log.json")
SCAN_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
if not SCAN_LOG_PATH.exists():
    SCAN_LOG_PATH.write_text("[]")

@app.get("/", response_class=HTMLResponse)
async def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BugHunter Dashboard</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    </head>
    <body>
        <section class="section">
            <div class="container">
                <h1 class="title">BugHunter Recon UI</h1>
                <form action="/scan" method="post">
                    <div class="field">
                        <label class="label">Target Domain</label>
                        <div class="control">
                            <input class="input" type="text" name="domain" placeholder="example.com" required>
                        </div>
                    </div>
                    <div class="control">
                        <button class="button is-link" type="submit">Start Scan</button>
                    </div>
                </form>
                <hr>
                <a class="button is-info" href="/results">View Scan Results</a>
            </div>
        </section>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/scan")
async def start_scan(domain: str = Form(...)):
    append_scan_log(domain, tools=["subfinder", "amass", "httpx", "nuclei", "ffuf"], status="running")

    def run_background():
        try:
            print(f"[+] Running scan for: {domain}")
            result = recon.run_full_recon(domain)
            print(f"[+] Recon result: {result}")
            update_scan_status(domain, status="complete", recon=result)
        except Exception as e:
            print(f"[!] Exception during scan: {e}")
            update_scan_status(domain, status="error", error=str(e))
    thread = threading.Thread(target=run_background)
    thread.start()

    return HTMLResponse(f"<html><body><h2>Scan started for {domain}</h2><a href='/'>Back</a></body></html>")

@app.get("/results")
async def get_results():
    data = load_scan_log()
    return JSONResponse(data)
