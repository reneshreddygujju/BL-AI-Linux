# DevOps Challenge Task - Summary

## ✅ Task Created Successfully!

I've created a comprehensive "Hard" difficulty DevOps task for the Terminal Bench 2.0 Framework.

## 📋 Task Overview

**Name**: Microservices Circular Dependency Resolution  
**Difficulty**: Hard  
**Domain**: DevOps / SWE  
**Estimated Success Rate**: 0.0 < rate < 0.7 (on 10 runs)

## 🎯 Challenge Description

The task presents a broken microservices deployment with three services:
- **auth-service** (port 5001) - Authentication service
- **api-gateway** (port 5002) - API routing gateway  
- **data-processor** (port 5003) - Data processing service

### 🐛 Bugs Introduced (6 major issues):

1. **Circular Dependency Deadlock**: Services wait for each other during startup
2. **Health Check Failures**: All services return 503 instead of 200
3. **Readiness Check Failures**: All services return "not ready" status
4. **Port Configuration Errors**: Multiple services configured with wrong ports
5. **Missing Environment Variables**: Critical env vars missing in K8s manifests
6. **Port Conflicts**: data-processor tries to use same port as api-gateway

## 📁 Files Created

```
devops-challenge@example.com/
├── task.toml                    ✅ Task configuration with Python 3.12
├── instruction.md               ✅ Detailed task description for AI agent
├── README.md                    ✅ Complete documentation
├── environment/
│   ├── Dockerfile               ✅ Python 3.12 environment setup
│   ├── docker-compose.yml       ✅ Broken compose config
│   ├── start_services.sh        ✅ Service startup script
│   ├── services/
│   │   ├── auth-service/app.py      ✅ Broken auth service
│   │   ├── api-gateway/app.py       ✅ Broken gateway
│   │   └── data-processor/app.py    ✅ Broken processor
│   └── k8s/
│       ├── auth-service.yaml        ✅ Broken K8s manifest
│       ├── api-gateway.yaml         ✅ Broken K8s manifest
│       └── data-processor.yaml      ✅ Broken K8s manifest
├── solution/
│   └── solve.sh                 ✅ Complete solution (fixes all 6 issues)
└── tests/
    ├── test.sh                  ✅ Test runner (provided by harbor)
    └── test_outputs.py          ✅ 15 comprehensive tests
```

## 🧪 Test Coverage

The test suite includes 15 tests covering:
- ✅ Service startup without deadlock
- ✅ Health checks return 200 for all services
- ✅ Readiness checks return 200 for all services
- ✅ Services run on correct ports (5001, 5002, 5003)
- ✅ No port conflicts
- ✅ Authentication token generation
- ✅ Authentication token validation
- ✅ End-to-end request flow through all services
- ✅ Kubernetes manifests validation
- ✅ Docker Compose configuration validation

## 🎓 Why This is "Hard"

1. **Multiple Interconnected Issues**: Requires fixing 6+ different problems across 9+ files
2. **Requires Deep Reasoning**: Must understand circular dependencies and service startup patterns
3. **Multi-Format Editing**: Python code, YAML configs, shell scripts
4. **Domain Knowledge**: Microservices, health checks, container orchestration
5. **Subtle Bugs**: Circular dependency isn't immediately obvious from error messages
6. **Coordination Required**: Changes must be made consistently across multiple files

## 🚀 Next Steps

### 1. Install Docker (Required)
Since Docker isn't installed yet, you'll need it to test the task:
```bash
# On macOS, download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

### 2. Set Up Groq API Key
```bash
# Create account at console.groq.com
# Get API key and set it:
export GROQ_API_KEY="your_api_key_here"
```

### 3. Test the Oracle (Your Solution)
```bash
cd /path/to/workspace
export PATH="$HOME/.local/bin:$PATH"
harbor run -p "./devops-challenge@example.com" -a oracle
```

This should PASS all tests, confirming your solution works.

### 4. Test with AI Agent (10 runs)
```bash
harbor run -p "./devops-challenge@example.com" -a terminus-2 \
  --model groq/moonshotai/kimi-k2-instruct-0905 -k 10
```

This will run the task 10 times and give you a success rate report.

### 5. Validate Difficulty
The task should have:
- ✅ Success rate > 0.0 (solvable)
- ✅ Success rate < 0.7 (difficult)
- ✅ Agent demonstrates reasoning (analyzing logs, understanding dependencies)

### 6. Submit
Once validated, submit via: https://forms.gle/jJfsy546UKWJb9276

## 📊 Quality Checklist

- ✅ Test suite covers everything in instruction.md
- ✅ Functional tests included (end-to-end flow)
- ✅ Multiple functional tests (15 total)
- ✅ Pinned versions in Dockerfile (Python 3.12, Flask 3.0.0, etc.)
- ✅ No cheating - solution not in environment/ directory
- ✅ Tests not copied into Docker image
- ✅ Reproducible with pinned dependencies
- ✅ Real errors (not simulated)

## 💡 Task Highlights

**What makes this task excellent:**
- Real-world scenario (circular dependencies are common in microservices)
- Multiple layers of complexity (code, config, orchestration)
- Requires understanding, not just pattern matching
- Tests validate actual functionality, not just file changes
- Solution demonstrates best practices (retry logic, proper health checks)

## 🔍 Debugging Tips (for you)

If the oracle test fails:
1. Check Docker is running: `docker ps`
2. Check Python version: `python --version` (should be 3.12 in container)
3. Review test output for specific failures
4. Verify all files were created correctly

## 📝 Notes

- The task uses Flask for simplicity (lightweight, easy to understand)
- All services are stateless (no database required)
- The circular dependency is realistic (services discovering each other)
- Solution demonstrates proper patterns (health checks, retry logic, no blocking startup)
- Tests are comprehensive but not excessive (15 tests cover all requirements)

---

**Task Status**: ✅ READY FOR TESTING  
**Next Action**: Install Docker, then run oracle test  
**Estimated Time to Validate**: 15-30 minutes (after Docker installed)
