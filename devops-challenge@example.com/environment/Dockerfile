FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask==3.0.0 \
    requests==2.31.0 \
    pyyaml==6.0.1 \
    pytest==7.4.3

# Copy all files to /app/
COPY services /app/services
COPY k8s /app/k8s
COPY docker-compose.yml /app/docker-compose.yml
COPY start_services.sh /app/start_services.sh

# Make scripts executable
RUN chmod +x /app/start_services.sh

# Expose ports for all services
EXPOSE 5001 5002 5003

CMD ["/bin/bash"]
