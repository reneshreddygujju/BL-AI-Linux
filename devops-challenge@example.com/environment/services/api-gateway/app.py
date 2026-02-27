from flask import Flask, jsonify, request
import requests
import os
import time

app = Flask(__name__)

# BUG: Circular dependency - api-gateway tries to validate with auth-service on startup
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001')
DATA_PROCESSOR_URL = os.getenv('DATA_PROCESSOR_URL', 'http://localhost:5003')

def validate_auth_service():
    """Validate auth service is available"""
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# BUG: This blocks startup waiting for auth-service
print("Waiting for Auth Service to be ready...")
while not validate_auth_service():
    print("Auth Service not ready, retrying...")
    time.sleep(2)

@app.route('/health', methods=['GET'])
def health():
    # BUG: Health check tries to call other services, causing timeout
    try:
        auth_health = requests.get(f"{AUTH_SERVICE_URL}/health", timeout=1)
        if auth_health.status_code != 200:
            return jsonify({"status": "unhealthy"}), 503
    except:
        return jsonify({"status": "unhealthy"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    # BUG: Missing proper readiness check
    return jsonify({"status": "not ready"}), 503

@app.route('/api/process', methods=['POST'])
def process_request():
    # Validate token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "No token provided"}), 401
    
    auth_response = requests.post(
        f"{AUTH_SERVICE_URL}/auth/validate",
        json={"token": token.replace('Bearer ', '')}
    )
    
    if auth_response.status_code != 200:
        return jsonify({"error": "Invalid token"}), 401
    
    # Forward to data processor
    data = request.json
    processor_response = requests.post(
        f"{DATA_PROCESSOR_URL}/process",
        json=data
    )
    
    return jsonify(processor_response.json())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port)
