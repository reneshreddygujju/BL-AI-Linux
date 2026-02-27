# Microservices Deployment Crisis

## Background
You've inherited a microservices application that's failing to deploy. The system consists of three services (auth-service, api-gateway, and data-processor) that have circular dependency issues and misconfigured health checks causing deployment failures.

## Problem
The deployment is stuck in a crash loop. The services are:
1. **auth-service** - Handles authentication, depends on api-gateway for service discovery
2. **api-gateway** - Routes requests, depends on auth-service for token validation
3. **data-processor** - Processes data, depends on both services

All three services are failing to start properly due to:
- Circular dependency deadlock (services waiting for each other)
- Incorrect health check configurations
- Missing environment variables
- Port conflicts in the deployment manifests

## Your Task
Fix the deployment configuration and service code to:
1. Break the circular dependency by implementing proper startup ordering and retry logic
2. Fix the health check endpoints so services can report ready status correctly
3. Correct the environment variable configurations
4. Resolve port conflicts in the Kubernetes manifests
5. Ensure all three services start successfully and can communicate

## Success Criteria
- All three services must start without errors
- Health checks must pass for all services
- Services must be able to communicate with each other
- The deployment must be stable (no crash loops)
- A test request through the api-gateway must successfully authenticate and process data

## Files Location
All configuration files and service code are located in `/app/`:
- `/app/services/auth-service/`
- `/app/services/api-gateway/`
- `/app/services/data-processor/`
- `/app/k8s/` - Kubernetes manifests
- `/app/docker-compose.yml` - Docker Compose configuration

## Hints
- Look for circular dependencies in service initialization
- Check health check endpoints and readiness probes
- Examine environment variable references
- Review port configurations in manifests
- Consider implementing retry logic with exponential backoff
