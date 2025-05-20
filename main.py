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
        data = json.load(f)
        live_hosts = data.get("results", [])
        if not live_hosts:
            print("[!] No live hosts found by httpx.")
        for host in live_hosts:
            scanner.run_all_scans(host)

    if args.analyze_js:
        print("[*] Running AI analysis on JavaScript files...")
        os.makedirs("data/jsfiles", exist_ok=True)
        analyze_js_directory("data/jsfiles")

if __name__ == "__main__":
    main()
