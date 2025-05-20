# Dockerfile
FROM debian:bookworm

# --- Install Python, Go, and required dependencies ---
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv python3-full git curl wget unzip chromium nmap libpcap-dev libpcap0.8 && \
    apt-get clean

# --- Set up Python virtual environment ---
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Install Go ---
RUN wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.24.0.linux-amd64.tar.gz && \
    rm go1.24.0.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:$PATH:$PATH"

# --- Install Go-based tools ---
RUN go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN go install github.com/owasp-amass/amass/v3/...@latest
RUN go install github.com/tomnomnom/gf@latest
RUN go install github.com/tomnomnom/assetfinder@latest
RUN go install github.com/tomnomnom/httprobe@latest
RUN go install github.com/projectdiscovery/httpx/cmd/httpx@latest
RUN go install github.com/hakluke/hakrawler@latest
RUN go install github.com/lc/gau/v2/cmd/gau@latest
RUN go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
RUN go install github.com/ffuf/ffuf@latest

# --- Install naabu manually ---
RUN git clone https://github.com/projectdiscovery/naabu.git /tmp/naabu && \
    cd /tmp/naabu/cmd/naabu && \
    go build -o /usr/local/bin/naabu main.go && \
    rm -rf /tmp/naabu

# --- Install Ollama and LLaMA3 model ---
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama run llama3 --help || true

# Optional: Expose Ollama API port
EXPOSE 11434

# Copy application source
COPY . .

# Auto-start Ollama and background summarizer
ENTRYPOINT ["bash", "-c", "ollama serve & exec python main.py"]
