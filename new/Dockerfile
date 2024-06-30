# Use the official Ollama image as the base
FROM ollama/ollama:latest

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy the Flask application
COPY app.py /app/app.py

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

#COPY prompts blueridge file
COPY prompts_blueridge.py /app/prompts_blueridge.py

# Install Flask and requests
RUN pip3 install -r requirements.txt

# Expose the Ollama API port and the Flask port
EXPOSE 11434 8080

# Copy the startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Use the startup script as the entrypoint
ENTRYPOINT ["/app/start.sh"]
