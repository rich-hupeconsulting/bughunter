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

def run_ffuf(domain):
    print("[+] Running ffuf with wordlist on:", domain)
    command = (
        f"ffuf -u {domain}/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt "
        f"-t 40 -o data/outputs/ffuf_{domain.replace('://','_')}.json -of json"
    )
    run_command(command)

def run_nuclei(domain):
    print("[+] Running nuclei on:", domain)
    output = run_command(f"echo {domain} | nuclei -silent -json")
    results = [json.loads(line) for line in output.splitlines() if line.strip().startswith('{')]
    write_json("nuclei", domain, results)

def run_hakrawler(domain):
    print("[+] Running hakrawler on:", domain)
    output = run_command(f"echo {domain} | hakrawler")
    urls = output.splitlines()
    write_json("hakrawler", domain, urls)

def run_all_scans(domain):
    run_hakrawler(domain)
    run_ffuf(domain)
    run_nuclei(domain)
    print("[*] Scanning phase complete.")
