#!/bin/bash

# Script to start all services for testing
# This simulates the deployment environment

echo "Starting microservices..."

# Start auth-service in background
cd /app/services/auth-service
export PORT=5001
export API_GATEWAY_URL=http://localhost:5002
python app.py &
AUTH_PID=$!

# Start api-gateway in background
cd /app/services/api-gateway
export PORT=5002
export AUTH_SERVICE_URL=http://localhost:5001
export DATA_PROCESSOR_URL=http://localhost:5003
python app.py &
GATEWAY_PID=$!

# Start data-processor in background
cd /app/services/data-processor
export PORT=5003
python app.py &
PROCESSOR_PID=$!

echo "Services started with PIDs: Auth=$AUTH_PID, Gateway=$GATEWAY_PID, Processor=$PROCESSOR_PID"
echo "Waiting for services to initialize..."

# Wait a bit for services to start
sleep 10

# Check if services are running
ps -p $AUTH_PID > /dev/null && echo "Auth service running" || echo "Auth service failed"
ps -p $GATEWAY_PID > /dev/null && echo "Gateway running" || echo "Gateway failed"
ps -p $PROCESSOR_PID > /dev/null && echo "Processor running" || echo "Processor failed"

# Keep script running
wait
