# scanner.py
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

def write_json(tool, target, output):
    os.makedirs("data/outputs", exist_ok=True)
    filename = f"data/outputs/{tool}_{target.replace('://','_').replace('/', '_')}.json"
    with open(filename, "w") as f:
        json.dump({
            "tool": tool,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "results": output
        }, f, indent=2)

def run_ffuf(domain):
    print("[+] Running ffuf with wordlist on:", domain)
    command = (
        f"ffuf -u {domain}/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt "
        f"-t 40 -of json"
    )
    output = run_command(command)
    try:
        parsed = json.loads(output)
    except:
        parsed = output
    write_json("ffuf", domain, parsed)

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

def run_naabu(ip):
    print("[+] Running naabu on:", ip)
    output = run_command(f"echo {ip} | naabu -silent")
    results = output.splitlines()
    write_json("naabu", ip, results)

def run_nmap(ip):
    print("[+] Running nmap on:", ip)
    output = run_command(f"nmap -T4 -sV {ip}")
    write_json("nmap", ip, output.splitlines())

def run_all_scans(domain):
    run_hakrawler(domain)
    run_ffuf(domain)
    run_nuclei(domain)
    print("[*] Scanning phase complete.")

def run_ip_scans(ip):
    run_naabu(ip)
    run_nmap(ip)
    print("[*] IP scanning phase complete.")