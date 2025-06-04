# main.py
import argparse
import os
import json
from modules import recon  # Module handles toolchain recon
from modules import scanner  # Module handles vuln discovery
from ai.openai_helper import analyze_js_directory

def main():
    parser = argparse.ArgumentParser(description="BugHunter: Automated Bug Bounty Recon Framework")
    parser.add_argument("domain", help="Target domain to scan")
    parser.add_argument("--analyze-js", action="store_true", help="Send collected JavaScript to OpenAI for analysis")
    args = parser.parse_args()

    print(f"[*] Starting recon on: {args.domain}")
    recon.run_full_recon(args.domain)

    print("[*] Scanning all live hosts...")
    with open("data/outputs/httpx_probed.json") as f:
        raw_hosts = json.load(f)["results"]

# Only include valid URLs
    live_hosts = [h for h in raw_hosts if isinstance(h, str) and h.startswith(("http://", "https://"))]

    if not live_hosts:
        print("[!] No live hosts found by httpx.")
    for host in live_hosts:
        clean_host = host.replace("https://", "").replace("http://", "")
        scanner.run_all_scans(clean_host)

    if args.analyze_js:
        print("[*] Running AI analysis on JavaScript files...")
        os.makedirs("data/jsfiles", exist_ok=True)
        analyze_js_directory("data/jsfiles")

if __name__ == "__main__":
    main()
