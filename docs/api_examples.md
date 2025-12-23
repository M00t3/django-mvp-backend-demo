# API Examples

## Auth

### Register
```bash
curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "password123"}'
```
*Response*: `{"token": "..."}`

## Products

### List Products (Requires Token)
```bash
curl -X GET http://localhost:8000/api/products/ \
     -H "Authorization: Token <your_token>"
```

### Search Products
```bash
curl -X GET http://localhost:8000/api/products/?search=Sample \
     -H "Authorization: Token <your_token>"
```

### Create Product
```bash
curl -X POST http://localhost:8000/api/products/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token <your_token>" \
     -d '{"name": "New Product", "description": "Desc", "price": 100.00, "stock": 50}'
```
