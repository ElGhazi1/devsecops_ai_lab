# 🚀 Deployment Guide

## Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Git

### Quick Start
```bash
# Clone repository
git clone <repo-url>
cd devsecops_ai_lab

# Start services
docker-compose up -d

# Verify health
curl http://localhost:8001/health  # OAuth2
curl http://localhost:8002/health  # API
curl http://localhost:8003/health  # LLM
```

### Environment Variables

Create `.env` file:
```bash
# OAuth2 Service
OAUTH2_SECRET_KEY=your-secret-key-change-in-prod

# API Backend
DATABASE_URL_API=postgresql://api_user:api_pass@postgres-api:5432/api_db

# LLM Service
MODEL_PATH=/app/models/bert_model

# Logging
LOG_LEVEL=INFO
```

### Database Initialization
```bash
# OAuth2 tables auto-created on startup
# API tables auto-created on startup

# Manual initialization (if needed)
docker-compose exec oauth2-service python -c "from models import Base; Base.metadata.create_all()"
```

## Production Deployment

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml devsecops
```

### Kubernetes
Create `k8s/` manifests:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-backend
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: api-backend
```

### AWS ECS
```bash
# Create cluster
aws ecs create-cluster --cluster-name devsecops

# Push images to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr-url>
docker tag api-backend:latest <ecr-url>/api-backend:latest
docker push <ecr-url>/api-backend:latest
```

## Monitoring & Logging

### Health Checks
All services expose `/health` endpoint:
```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### Container Logs
```bash
# View logs
docker-compose logs -f service-name

# Filter logs
docker-compose logs -f oauth2-service | grep ERROR
```

## Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  api-backend:
    deploy:
      replicas: 3
```

### Load Balancing
Use Nginx/HAProxy in front of services.

## Security Considerations

- ✅ Use TLS/HTTPS in production
- ✅ Rotate secrets regularly
- ✅ Enable database encryption
- ✅ Use secrets management (AWS Secrets Manager, HashiCorp Vault)
- ✅ Implement WAF (Web Application Firewall)
- ✅ Set up monitoring and alerting

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL backup
docker-compose exec postgres-oauth pg_dump -U oauth_user oauth_db > backup.sql

# Restore
docker-compose exec -T postgres-oauth psql -U oauth_user oauth_db < backup.sql
```

### Model Checkpoints
```bash
# Backup BERT model
tar -czf bert_model_backup.tar.gz data/models/

# Restore
tar -xzf bert_model_backup.tar.gz
```

## Rollback Procedure

```bash
# Stop current services
docker-compose down

# Restore previous version
git checkout v1.0.0

# Restart services
docker-compose up -d
```
