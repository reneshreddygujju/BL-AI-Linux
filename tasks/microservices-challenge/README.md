# Microservices Circular Dependency Challenge

## Overview
This is a "Hard" difficulty DevOps task for the Terminal Bench 2.0 Framework. The challenge involves fixing a broken microservices deployment with multiple interconnected issues.

## Task Complexity
This task is designed to be challenging because it requires:
1. **Understanding circular dependencies** - Services wait for each other during startup
2. **Debugging health checks** - Multiple services return wrong status codes
3. **Port configuration issues** - Services configured with wrong ports
4. **Environment variable problems** - Missing or incorrect environment variables
5. **Multi-file coordination** - Fixes required across Python code, Docker Compose, and Kubernetes manifests

## Problem Summary
The system has 3 microservices:
- **auth-service** (port 5001) - Authentication
- **api-gateway** (port 5002) - API routing
- **data-processor** (port 5003) - Data processing

### Bugs Introduced:
1. **Circular Dependency Deadlock**: auth-service waits for api-gateway, api-gateway waits for auth-service
2. **Health Check Failures**: Services return 503 instead of 200
3. **Port Conflicts**: data-processor configured to use port 5002 (conflicts with api-gateway)
4. **Missing Environment Variables**: api-gateway missing AUTH_SERVICE_URL in K8s manifest
5. **Wrong Port Configurations**: Multiple services have PORT env var set incorrectly

## Solution Approach
The solution must:
1. Remove blocking startup validation that causes circular dependencies
2. Fix health check endpoints to return 200 status
3. Fix readiness check endpoints to return 200 status
4. Correct all port configurations (5001, 5002, 5003)
5. Add missing environment variables
6. Fix Kubernetes manifest port mappings
7. Fix Docker Compose port mappings and remove circular depends_on

## Testing
The test suite validates:
- All services start successfully (no deadlock)
- Health checks return 200 for all services
- Readiness checks return 200 for all services
- Services run on correct ports
- Authentication flow works
- End-to-end request processing works
- Kubernetes manifests are correctly configured
- Docker Compose is correctly configured

## Difficulty Justification
This task meets "Hard" criteria because:
- **Multiple interconnected issues**: Requires fixing 6+ different problems
- **Requires reasoning**: Agent must understand circular dependencies and service startup order
- **Multi-file changes**: Requires editing 9+ files across different formats (Python, YAML, shell)
- **Domain knowledge**: Requires understanding of microservices, health checks, and container orchestration
- **Not obvious**: The circular dependency issue is subtle and requires careful analysis

## Expected Success Rate
Target: 0.0 < success rate < 0.7 on 10 runs with standard LLM agent

The task is solvable but requires:
- Careful log analysis
- Understanding of service dependencies
- Knowledge of health check patterns
- Ability to coordinate changes across multiple files
- Understanding of both Docker Compose and Kubernetes configurations

## Files Structure
```
devops-challenge@example.com/
├── instruction.md              # Task description for the agent
├── task.toml                   # Task configuration
├── environment/
│   ├── Dockerfile              # Container setup
│   ├── docker-compose.yml      # Docker Compose config (broken)
│   ├── start_services.sh       # Service startup script
│   ├── services/
│   │   ├── auth-service/
│   │   │   └── app.py          # Auth service (broken)
│   │   ├── api-gateway/
│   │   │   └── app.py          # API Gateway (broken)
│   │   └── data-processor/
│   │       └── app.py          # Data processor (broken)
│   └── k8s/
│       ├── auth-service.yaml   # K8s manifest (broken)
│       ├── api-gateway.yaml    # K8s manifest (broken)
│       └── data-processor.yaml # K8s manifest (broken)
├── solution/
│   └── solve.sh                # Complete solution script
└── tests/
    ├── test.sh                 # Test runner
    └── test_outputs.py         # Comprehensive test suite
```

## Running the Task

### Prerequisites
- Docker installed and running
- Harbor CLI installed (`uv tool install harbor`)
- Groq API key set up

### Test the Oracle (Your Solution)
```bash
harbor run -p "./devops-challenge@example.com" -a oracle
```

### Test with AI Agent
```bash
harbor run -p "./devops-challenge@example.com" -a terminus-2 --model groq/moonshotai/kimi-k2-instruct-0905 -k 10
```

## Notes
- The task uses Python 3.12 as specified in task.toml
- All services use Flask for simplicity
- The solution demonstrates proper microservices patterns
- Tests are comprehensive and cover all requirements
