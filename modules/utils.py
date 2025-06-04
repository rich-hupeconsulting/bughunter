import json
import os

SCAN_LOG_PATH = "data/scan_log.json"

def write_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def read_json(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def load_scan_log():
    if not os.path.exists(SCAN_LOG_PATH):
        return []
    with open(SCAN_LOG_PATH, 'r') as f:
        return json.load(f)

def append_scan_log(domain, tools, status):
    log = load_scan_log()
    log.append({
        "target": domain,
        "tools": tools,
        "status": status
    })
    with open("data/scan_log.json", "w") as f:
        json.dump(log, f, indent=2)


def update_scan_status(target, status=None, recon=None, error=None):
    log = load_scan_log()
    for entry in log:
        if entry["target"] == target and entry["status"] in ["running", "queued"]:
            if status:
                entry["status"] = status
            if recon is not None:
                entry["recon"] = recon
            if error:
                entry["error"] = error
            break
    write_json(SCAN_LOG_PATH, log)
