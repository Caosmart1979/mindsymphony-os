---
name: devops-workflow-designer
description: Expert DevOps workflow and CI/CD pipeline design guidance. Use this skill when setting up CI/CD pipelines, automating deployments, configuring infrastructure as code, implementing monitoring/alerting, containerizing applications, managing cloud resources, or improving development workflows.
license: Apache-2.0
interop_metadata:
  skill_id: skills.devops_workflow_designer
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# DevOps Workflow Designer

Expert guidance for building efficient, automated development and operations workflows.

## CI/CD Pipeline Design

**Pipeline Stages:**
```
Code → Build → Test → Deploy → Monitor
```

**GitHub Actions Example:**
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: kubectl set image deployment/app app=app:${{ github.sha }}
```

## Infrastructure as Code

### Terraform
```hcl
resource "aws_instance" "app" {
  ami           = "ami-12345"
  instance_type = "t3.micro"
  
  tags = {
    Name = "app"
    Environment = terraform.workspace
  }
}
```

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 3000
```

## Deployment Strategies

**Blue-Green:** Zero-downtime with two environments
**Canary:** Gradual rollout to subset of users
**Rolling:** Incremental replacement of instances

## Monitoring

**Prometheus Metrics:**
```javascript
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});
```

**Structured Logging:**
```javascript
logger.info('user_logged_in', {
  user_id: userId,
  timestamp: new Date().toISOString(),
  ip: req.ip
});
```

## Best Practices

✅ **Do:**
- Use infrastructure as code
- Automate everything
- Monitor and alert proactively
- Document runbooks
- Test disaster recovery

❌ **Don't:**
- Store secrets in code
- Skip security scanning
- Ignore cost monitoring
- Manual deployments
- Neglect documentation

## Working with This Skill

Provide:
1. Cloud provider (AWS, GCP, Azure)
2. Application type
3. Team size and expertise
4. Deployment requirements
5. Compliance requirements
