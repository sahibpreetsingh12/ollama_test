#!/bin/bash

# Start Ollama service in the background
ollama serve &

# Wait for Ollama service to start
sleep 10

# Pull the phi model
ollama pull mannix/defog-llama3-sqlcoder-8b:latest

# Start the Flask application
python3 /app/app.py
