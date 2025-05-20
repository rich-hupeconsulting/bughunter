import subprocess
import json
import os
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def write_json(tool, domain, output):
    os.makedirs("data/outputs", exist_ok=True)
    filename = f"data/outputs/{tool}_{domain}.json"
    with open(filename, "w") as f:
        json.dump({
            "tool": tool,
            "target": domain,
            "timestamp": datetime.utcnow().isoformat(),
            "results": output
        }, f, indent=2)

def run_subfinder(domain):
    print("[+] Running subfinder...")
    output = run_command(f"subfinder -d {domain} -silent")
    subdomains = output.splitlines()
    write_json("subfinder", domain, subdomains)
    return subdomains

def run_amass(domain):
    print("[+] Running amass enum...")
    output = run_command(f"amass enum -passive -d {domain}")
    subdomains = output.splitlines()
    write_json("amass", domain, subdomains)
    return subdomains

def run_gau(domain):
    print("[+] Running gau...")
    output = run_command(f"gau {domain}")
    urls = output.splitlines()
    write_json("gau", domain, urls)
    return urls

def run_httpx(subdomains):
    print("[+] Probing with httpx...")
    with open("temp_subs.txt", "w") as f:
        f.write("\n".join(subdomains))
    output = run_command("httpx -silent -l temp_subs.txt")
    os.remove("temp_subs.txt")
    live_hosts = output.splitlines()
    write_json("httpx", "probed", live_hosts)
    return live_hosts

def run_full_recon(domain):
    subs1 = run_subfinder(domain)
    subs2 = run_amass(domain)
    all_subs = list(set(subs1 + subs2))
    live_hosts = run_httpx(all_subs)
    gau_urls = run_gau(domain)
    print(f"[*] Recon complete. Found {len(all_subs)} unique subdomains and {len(gau_urls)} historical URLs.")
