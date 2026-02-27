from flask import Flask, jsonify, request
import requests
import os
import time

app = Flask(__name__)

# BUG: Circular dependency - auth-service tries to validate with api-gateway on startup
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL', 'http://localhost:5002')

def validate_with_gateway():
    """Validate service registration with API gateway"""
    try:
        response = requests.get(f"{API_GATEWAY_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# BUG: This blocks startup waiting for api-gateway
print("Waiting for API Gateway to be ready...")
while not validate_with_gateway():
    print("API Gateway not ready, retrying...")
    time.sleep(2)

@app.route('/health', methods=['GET'])
def health():
    # BUG: Health check always returns 503
    return jsonify({"status": "unhealthy"}), 503

@app.route('/ready', methods=['GET'])
def ready():
    # BUG: Missing readiness check
    return jsonify({"status": "not ready"}), 503

@app.route('/auth/validate', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if token == 'valid-token-123':
        return jsonify({"valid": True, "user": "test-user"})
    return jsonify({"valid": False}), 401

@app.route('/auth/token', methods=['POST'])
def generate_token():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'admin' and password == 'secret':
        return jsonify({"token": "valid-token-123"})
    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    # BUG: Wrong port configuration
    port = int(os.getenv('PORT', 5002))  # Should be 5001
    app.run(host='0.0.0.0', port=port)
