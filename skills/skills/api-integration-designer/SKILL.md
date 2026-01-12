---
name: api-integration-designer
description: Expert API design and integration guidance. Use this skill when designing REST APIs, GraphQL schemas, integrating third-party services, implementing authentication (OAuth, JWT, API keys), handling rate limiting, creating API clients, or working with webhooks and real-time data streams.
license: Apache-2.0
interop_metadata:
  skill_id: skills.api_integration_designer
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# API Integration Designer

Expert guidance for designing robust APIs and integrating services effectively. This skill helps you create production-grade API integrations that are secure, scalable, and maintainable.

## Core Principles

**API Design Excellence:**
- Clear, consistent naming conventions for endpoints and operations
- Proper HTTP method usage (GET, POST, PUT, PATCH, DELETE)
- Meaningful status codes and error responses
- Comprehensive documentation with examples
- Versioning strategy from day one

**Security First:**
- Implement proper authentication (OAuth 2.0, JWT, API keys)
- Use HTTPS exclusively in production
- Validate and sanitize all inputs
- Implement rate limiting and throttling
- Secure sensitive data with environment variables

**Reliability & Performance:**
- Exponential backoff for retries
- Request/response caching where appropriate
- Connection pooling and keep-alive
- Timeout configurations for all requests

## Authentication Strategies

### JWT (JSON Web Tokens)
```javascript
{
  "sub": "user_id",
  "iat": 1234567890,
  "exp": 1234567890,
  "roles": ["user", "admin"]
}
```

### OAuth 2.0 Flow
1. Authorization Code flow for server-side apps
2. PKCE (Proof Key for Code Exchange) for mobile/SPA
3. Client Credentials for service-to-service

## Common Pitfalls to Avoid

❌ **Don't:**
- Hardcode API keys or credentials
- Ignore error responses from third-party APIs
- Make unlimited requests without rate limiting
- Expose sensitive data in error messages

✅ **Do:**
- Use environment variables for secrets
- Implement comprehensive error handling
- Add monitoring and alerting
- Validate all data before use

## Working with This Skill

When using this skill, provide:
1. The type of API/integration you're building
2. Authentication requirements
3. Data structures and endpoints
4. Programming language and framework
