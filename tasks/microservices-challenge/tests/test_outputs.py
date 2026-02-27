import pytest
import requests
import time
import subprocess
import os
import signal

def wait_for_service(url, timeout=30):
    """Wait for a service to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def services():
    """Start all services and wait for them to be ready"""
    # Start services in background
    processes = []
    
    # Start auth-service
    env_auth = os.environ.copy()
    env_auth.update({
        'PORT': '5001',
        'API_GATEWAY_URL': 'http://localhost:5002'
    })
    p1 = subprocess.Popen(
        ['python', '/app/services/auth-service/app.py'],
        env=env_auth,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(p1)
    
    # Start api-gateway
    env_gateway = os.environ.copy()
    env_gateway.update({
        'PORT': '5002',
        'AUTH_SERVICE_URL': 'http://localhost:5001',
        'DATA_PROCESSOR_URL': 'http://localhost:5003'
    })
    p2 = subprocess.Popen(
        ['python', '/app/services/api-gateway/app.py'],
        env=env_gateway,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(p2)
    
    # Start data-processor
    env_processor = os.environ.copy()
    env_processor.update({
        'PORT': '5003'
    })
    p3 = subprocess.Popen(
        ['python', '/app/services/data-processor/app.py'],
        env=env_processor,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    processes.append(p3)
    
    # Wait for services to start
    time.sleep(5)
    
    # Check if all processes are still running
    for p in processes:
        assert p.poll() is None, f"Service process {p.pid} died during startup"
    
    yield processes
    
    # Cleanup
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=5)
        except:
            p.kill()

def test_auth_service_health(services):
    """Test that auth-service health endpoint returns 200"""
    assert wait_for_service('http://localhost:5001/health', timeout=30), \
        "Auth service health check failed to return 200"
    
    response = requests.get('http://localhost:5001/health')
    assert response.status_code == 200, \
        f"Auth service health check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'healthy', \
        "Auth service health status is not 'healthy'"

def test_auth_service_ready(services):
    """Test that auth-service readiness endpoint returns 200"""
    response = requests.get('http://localhost:5001/ready')
    assert response.status_code == 200, \
        f"Auth service readiness check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'ready', \
        "Auth service readiness status is not 'ready'"

def test_api_gateway_health(services):
    """Test that api-gateway health endpoint returns 200"""
    assert wait_for_service('http://localhost:5002/health', timeout=30), \
        "API Gateway health check failed to return 200"
    
    response = requests.get('http://localhost:5002/health')
    assert response.status_code == 200, \
        f"API Gateway health check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'healthy', \
        "API Gateway health status is not 'healthy'"

def test_api_gateway_ready(services):
    """Test that api-gateway readiness endpoint returns 200"""
    response = requests.get('http://localhost:5002/ready')
    assert response.status_code == 200, \
        f"API Gateway readiness check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'ready', \
        "API Gateway readiness status is not 'ready'"

def test_data_processor_health(services):
    """Test that data-processor health endpoint returns 200"""
    assert wait_for_service('http://localhost:5003/health', timeout=30), \
        "Data processor health check failed to return 200"
    
    response = requests.get('http://localhost:5003/health')
    assert response.status_code == 200, \
        f"Data processor health check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'healthy', \
        "Data processor health status is not 'healthy'"

def test_data_processor_ready(services):
    """Test that data-processor readiness endpoint returns 200"""
    response = requests.get('http://localhost:5003/ready')
    assert response.status_code == 200, \
        f"Data processor readiness check returned {response.status_code}, expected 200"
    assert response.json()['status'] == 'ready', \
        "Data processor readiness status is not 'ready'"

def test_services_running_on_correct_ports(services):
    """Test that all services are running on their correct ports"""
    # Auth service on 5001
    try:
        response = requests.get('http://localhost:5001/health', timeout=2)
        assert response.status_code == 200, "Auth service not on port 5001"
    except:
        pytest.fail("Auth service not accessible on port 5001")
    
    # API Gateway on 5002
    try:
        response = requests.get('http://localhost:5002/health', timeout=2)
        assert response.status_code == 200, "API Gateway not on port 5002"
    except:
        pytest.fail("API Gateway not accessible on port 5002")
    
    # Data processor on 5003
    try:
        response = requests.get('http://localhost:5003/health', timeout=2)
        assert response.status_code == 200, "Data processor not on port 5003"
    except:
        pytest.fail("Data processor not accessible on port 5003")

def test_no_circular_dependency_deadlock(services):
    """Test that services start without circular dependency deadlock"""
    # If we reach here, services have started successfully
    # This test passes if all services are running
    for i, p in enumerate(services):
        assert p.poll() is None, \
            f"Service {i} died, indicating possible circular dependency issue"

def test_auth_token_generation(services):
    """Test authentication token generation"""
    wait_for_service('http://localhost:5001/health', timeout=30)
    
    response = requests.post(
        'http://localhost:5001/auth/token',
        json={'username': 'admin', 'password': 'secret'}
    )
    assert response.status_code == 200, \
        f"Token generation failed with status {response.status_code}"
    assert 'token' in response.json(), "Token not in response"
    assert response.json()['token'] == 'valid-token-123', "Invalid token returned"

def test_auth_token_validation(services):
    """Test authentication token validation"""
    wait_for_service('http://localhost:5001/health', timeout=30)
    
    response = requests.post(
        'http://localhost:5001/auth/validate',
        json={'token': 'valid-token-123'}
    )
    assert response.status_code == 200, \
        f"Token validation failed with status {response.status_code}"
    assert response.json()['valid'] == True, "Token validation returned invalid"

def test_end_to_end_request_flow(services):
    """Test complete request flow through all services"""
    # Wait for all services
    wait_for_service('http://localhost:5001/health', timeout=30)
    wait_for_service('http://localhost:5002/health', timeout=30)
    wait_for_service('http://localhost:5003/health', timeout=30)
    
    # Get auth token
    auth_response = requests.post(
        'http://localhost:5001/auth/token',
        json={'username': 'admin', 'password': 'secret'}
    )
    assert auth_response.status_code == 200, "Failed to get auth token"
    token = auth_response.json()['token']
    
    # Make request through API gateway
    response = requests.post(
        'http://localhost:5002/api/process',
        headers={'Authorization': f'Bearer {token}'},
        json={'message': 'test data'}
    )
    assert response.status_code == 200, \
        f"End-to-end request failed with status {response.status_code}"
    
    result = response.json()
    assert result['processed'] == True, "Data not processed"
    assert 'test data' in result['result'], "Data not correctly processed"

def test_kubernetes_manifests_valid():
    """Test that Kubernetes manifests have correct configurations"""
    import yaml
    
    # Check auth-service manifest
    with open('/app/k8s/auth-service.yaml', 'r') as f:
        auth_manifest = list(yaml.safe_load_all(f))
    
    deployment = auth_manifest[0]
    assert deployment['spec']['template']['spec']['containers'][0]['env'][0]['value'] == '5001', \
        "Auth service PORT env var not set to 5001 in K8s manifest"
    
    # Check api-gateway manifest
    with open('/app/k8s/api-gateway.yaml', 'r') as f:
        gateway_manifest = list(yaml.safe_load_all(f))
    
    deployment = gateway_manifest[0]
    env_vars = {e['name']: e['value'] for e in deployment['spec']['template']['spec']['containers'][0]['env']}
    assert 'AUTH_SERVICE_URL' in env_vars, \
        "AUTH_SERVICE_URL missing from api-gateway K8s manifest"
    assert env_vars['AUTH_SERVICE_URL'] == 'http://auth-service:5001', \
        "AUTH_SERVICE_URL has wrong value in K8s manifest"
    
    # Check data-processor manifest
    with open('/app/k8s/data-processor.yaml', 'r') as f:
        processor_manifest = list(yaml.safe_load_all(f))
    
    deployment = processor_manifest[0]
    assert deployment['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] == 5003, \
        "Data processor containerPort not set to 5003 in K8s manifest"
    assert deployment['spec']['template']['spec']['containers'][0]['env'][0]['value'] == '5003', \
        "Data processor PORT env var not set to 5003 in K8s manifest"
    
    service = processor_manifest[1]
    assert service['spec']['ports'][0]['targetPort'] == 5003, \
        "Data processor service targetPort not set to 5003 in K8s manifest"

def test_docker_compose_valid():
    """Test that docker-compose.yml has correct configurations"""
    import yaml
    
    with open('/app/docker-compose.yml', 'r') as f:
        compose = yaml.safe_load(f)
    
    # Check no circular dependencies
    assert 'depends_on' not in compose['services']['auth-service'] or \
           'api-gateway' not in compose['services']['auth-service'].get('depends_on', []), \
           "Circular dependency: auth-service depends on api-gateway"
    
    assert 'depends_on' not in compose['services']['api-gateway'] or \
           'auth-service' not in compose['services']['api-gateway'].get('depends_on', []), \
           "Circular dependency: api-gateway depends on auth-service"
    
    # Check data-processor port configuration
    assert compose['services']['data-processor']['environment'][0] == 'PORT=5003', \
        "Data processor PORT not set to 5003 in docker-compose"
    assert '5003:5003' in compose['services']['data-processor']['ports'], \
        "Data processor port mapping not 5003:5003 in docker-compose"
