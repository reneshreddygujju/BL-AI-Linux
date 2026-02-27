from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    # BUG: Returns wrong status code
    return jsonify({"status": "healthy"}), 503

@app.route('/ready', methods=['GET'])
def ready():
    # BUG: Always returns not ready
    return jsonify({"status": "not ready"}), 503

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    # Simple data processing
    result = {
        "processed": True,
        "data": data,
        "result": f"Processed: {data.get('message', 'no message')}"
    }
    return jsonify(result)

if __name__ == '__main__':
    # BUG: Wrong port - conflicts with api-gateway
    port = int(os.getenv('PORT', 5002))  # Should be 5003
    app.run(host='0.0.0.0', port=port)
