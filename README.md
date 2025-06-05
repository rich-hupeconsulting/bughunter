# bughunter
BugHunter – Bug Bounty Recon Dashboard
BugHunter is an extensible, Dockerized recon tool for bug bounty hunting and offensive security. It automates common reconnaissance tasks, provides live scan feedback, and includes a lightweight web interface to manage and monitor scan results.

Features
Subdomain Enumeration (Subfinder, Amass)

Live Host Detection (HTTPX)

Historical URL Gathering (gau)

Vulnerability Detection (Nuclei, FFUF-ready)

JSON Logging & Live Status Updates

Web Dashboard (FastAPI + Bulma)

Easy Docker Deployment

Installation
1. Clone the Repository
git clone https://github.com/youruser/bughunter.git
cd bughunter
2. Build the Docker Image
docker build -t bughunter .
Running the Application
docker run -p 8000:8000 \
  -v $(pwd):/app \
  -v /etc/hosts:/etc/hosts:ro \
  bughunter
Access the web interface at:
http://localhost:8000

Web Interface
Use the browser-based dashboard to:

Start scans for any target domain

View current and historical scan results (subdomains, live hosts, URLs)

Monitor scan progress in real time

Recon Tools Used
Tool	Purpose
subfinder	Fast passive subdomain enumeration
amass	Deep passive/active subdomain scan
httpx	Probing HTTP/HTTPS services
gau	Collect historical URLs
nuclei	(Planned) Custom vulnerability scans
ffuf	(Planned) Fuzzing paths & parameters

Directory Structure
bughunter/
├── Dockerfile
├── serve.py                  # Web server and UI
├── modules/
│   ├── recon.py              # Main recon logic
│   ├── scanner.py            # Individual tool wrappers
│   └── utils.py              # Logging and helpers
├── data/
│   ├── scan_log.json         # Log of all scans
│   └── outputs/              # Raw output from tools
└── static/                   # CSS and JS assets
Dependencies (inside Docker)
Python 3.10+

FastAPI

Subfinder

Amass

HTTPX CLI

gau

nuclei

ffuf

All required tools and packages are installed automatically via the Dockerfile.

API Endpoints
Method	Endpoint	Description
GET	/	Homepage and scan input form
POST	/scan	Trigger a new scan
GET	/results	Return JSON log of all scans

Roadmap
Add Nuclei integration

Add FFUF wordlist fuzzing

Add user authentication

Add graphical recon map or topology

Add export options (PDF/Markdown/JSON)

Contributions
Pull requests are welcome. Please ensure changes are tested and formatted according to PEP8 standards.

Disclaimer
This software is intended for authorized security testing and educational purposes only. Do not use this tool on systems without explicit permission.

Author
Developed by Hupe Consulting
Contact: richard@hupeconsulting.co.uk

