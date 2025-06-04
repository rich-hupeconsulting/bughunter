#!/bin/bash

# Start Ollama server in background
ollama serve &

# Wait a few seconds to let Ollama initialize
sleep 3

# Start FastAPI properly and expose it
exec uvicorn serve:app --host 0.0.0.0 --port 8000
