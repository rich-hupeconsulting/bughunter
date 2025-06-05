# modules/recon.py

import os
from modules.scanner import (
    run_subfinder,
    run_amass,
    run_httpx,
    run_gau,
    write_json,
)

def run_full_recon(domain):
    print(f"[+] Starting recon on: {domain}")
    os.makedirs("data/outputs", exist_ok=True)

    # Step 1: Find subdomains
    print("[+] Running subfinder...")
    subfinder_results = run_subfinder(domain)

    print("[+] Running amass enum...")
    amass_results = run_amass(domain)

    all_subdomains = set(subfinder_results + amass_results)
    all_subdomains = sorted(all_subdomains)

    # Save subdomains
    write_json("recon_subdomains", domain, all_subdomains)

    # Step 2: Probe live hosts
    print("[+] Probing with httpx...")
    live_hosts = run_httpx(all_subdomains)
    write_json("httpx_live", domain, live_hosts)

    # Step 3: Fetch historical URLs
    print("[+] Running gau...")
    urls = run_gau(domain)
    write_json("gau_urls", domain, urls)

    print("[*] Recon complete.")
    return {
        "subdomains": all_subdomains,
        "live_hosts": live_hosts,
        "urls": urls,
    }
