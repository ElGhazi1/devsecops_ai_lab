# 📡 API Documentation

## Authentication

All endpoints (except `/health`, `/register`, `/token`) require OAuth2 Bearer token.

### Register
```bash
POST /register
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure_password"
}

Response: 200 OK
{
  "id": 1,
  "username": "user@example.com"
}
```

### Login
```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## OAuth2 Service (Port 8001)

### Health Check
```bash
GET /health

Response: 200 OK
{
  "status": "healthy",
  "service": "oauth2-service"
}
```

### Get Current User
```bash
GET /me
Authorization: Bearer {token}

Response: 200 OK
{
  "id": 1,
  "username": "user@example.com"
}
```

## API Backend (Port 8002)

### Create Product
```bash
POST /products
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Product Name",
  "description": "Product Description",
  "price": 99.99
}

Response: 201 Created
{
  "id": 1,
  "name": "Product Name",
  "description": "Product Description",
  "price": 99.99,
  "owner_id": 1,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Products
```bash
GET /products
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "name": "Product Name",
    "price": 99.99
  }
]
```

## LLM/NLP Service (Port 8003)

### Detect Threat
```bash
POST /detect-threat
Content-Type: application/json

{
  "text": "SELECT * FROM users",
  "threshold": 0.7
}

Response: 200 OK
{
  "text": "SELECT * FROM users",
  "is_threat": true,
  "confidence": 0.95,
  "threat_type": "injection"
}
```

### Batch Threat Detection
```bash
POST /detect-threats-batch
Content-Type: application/json

{
  "texts": [
    "normal query",
    "DROP TABLE users",
    "'; DELETE FROM orders; --"
  ],
  "threshold": 0.7
}

Response: 200 OK
{
  "results": [
    {"text": "normal query", "is_threat": false, "confidence": 0.15, "threat_type": "other"},
    {"text": "DROP TABLE users", "is_threat": true, "confidence": 0.98, "threat_type": "injection"},
    {"text": "'; DELETE...", "is_threat": true, "confidence": 0.97, "threat_type": "injection"}
  ],
  "total_processed": 3,
  "threats_detected": 2
}
```

### Model Stats
```bash
GET /model-stats

Response: 200 OK
{
  "model_name": "bert-base-uncased",
  "num_labels": 2,
  "labels": ["safe", "threat"],
  "max_length": 512,
  "framework": "PyTorch"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
