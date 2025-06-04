# modules/scanner.py

import subprocess
import json
import os
from datetime import datetime


def run_command(command):
    """Executes a shell command and returns its stdout."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=300
        )
        if result.stderr:
            print(f"[!] Error: {result.stderr.strip()}")
        return result.stdout.strip()
    except Exception as e:
        print(f"[!] Exception while running command: {e}")
        return ""


def write_json(tool, domain, output):
    """Writes output data to JSON file under data/outputs."""
    safe_name = domain.replace("://", "_").replace("/", "_").replace(".", "_")
    filename = f"data/outputs/{tool}_{safe_name}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump({
            "tool": tool,
            "target": domain,
            "timestamp": datetime.utcnow().isoformat(),
            "results": output
        }, f, indent=2)


def run_subfinder(domain):
    """Runs subfinder for passive subdomain enumeration."""
    print("[+] Running subfinder...")
    output = run_command(f"subfinder -silent -d {domain}")
    return output.splitlines() if output else []


def run_amass(domain):
    """Runs amass enum for deeper subdomain enumeration."""
    print("[+] Running amass...")
    output = run_command(f"amass enum -silent -d {domain}")
    return output.splitlines() if output else []


def run_httpx(subdomains):
    """Probes subdomains for live HTTP/S services."""
    print("[+] Running httpx...")
    if not subdomains:
        return []

    joined = "\n".join(subdomains)
    command = f"echo '{joined}' | httpx -silent"
    output = run_command(command)
    return output.splitlines() if output else []


def run_gau(domain):
    """Fetches historical URLs using gau."""
    print("[+] Running gau...")
    output = run_command(f"gau {domain}")
    return output.splitlines() if output else []
