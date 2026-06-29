# E-Commerce Backend API

A production-ready REST API built with **FastAPI** and **MongoDB**, following clean architecture principles.

---

## Features

- Full product catalogue CRUD
- Inventory management with stock tracking
- Shopping cart per user
- Order placement with automatic stock decrement
- Payment processing
- Centralized error handling & logging
- Swagger / ReDoc documentation
- Fully mocked unit test suite

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.111 |
| Database | MongoDB (pymongo) |
| Validation | Pydantic v2 |
| Config | pydantic-settings |
| Testing | pytest + httpx |
| Server | Uvicorn |

---

## Architecture

```
Request → Route → Service → MongoDB Collection
                     ↑
              Pydantic Model (validation)
```

- **Routes** – HTTP interface only, no business logic
- **Services** – All business logic, no HTTP concerns
- **Models** – Pydantic request/response schemas
- **Database** – Single MongoClient singleton, injected via FastAPI `Depends`
- **Exceptions** – Custom error classes + global handlers
- **Logger** – Structured stdout logging across all layers

---

## Folder Structure

```
backend/
├── app/
│   ├── api/routes/          # One file per domain
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── database/            # MongoDB connection + collection accessors
│   ├── config.py            # Settings from .env
│   ├── dependencies.py      # FastAPI Depends callables
│   ├── exceptions.py        # Custom exceptions + handlers
│   ├── logger.py            # Shared logger factory
│   └── main.py              # App factory
├── tests/                   # pytest test suite
├── .env                     # Environment variables
├── requirements.txt
└── pytest.ini
```

---

## Installation

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

---

## Environment Variables

Copy `.env` and fill in your values:

```env
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
DATABASE_NAME=ecommerce_db
SECRET_KEY=your-secret-key
DEBUG=false
```

---

## Running the API

```bash
cd backend
uvicorn app.main:app --reload
```

API available at: `http://127.0.0.1:8000`
Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create product |
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product by ID |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| POST | `/inventory` | Add inventory record |
| GET | `/inventory/{product_id}` | Get stock level |
| PUT | `/inventory/{product_id}?stock=N` | Update stock |
| POST | `/cart` | Add item to cart |
| GET | `/cart/{user_id}` | Get user's cart |
| DELETE | `/cart/{cart_id}` | Remove cart item |
| POST | `/payments` | Process payment |
| GET | `/payments` | List payments |
| POST | `/orders` | Place order |
| GET | `/orders` | List all orders |
| GET | `/orders/{id}` | Get order by ID |

---

## Testing

```bash
cd backend
pytest
```

Tests are fully isolated — MongoDB is mocked using `unittest.mock.MagicMock`. No live database required.

---

## Sample Requests

**Create a product**
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Headphones","description":"Wireless","category":"Electronics","price":49.99}'
```

**Place an order**
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","product_id":"<product_id>","quantity":1,"amount":49.99}'
```

---

## MongoDB Collections

| Collection | Purpose |
|-----------|---------|
| `products` | Product catalogue |
| `inventory` | Stock levels per product |
| `cart` | User cart items |
| `orders` | Placed orders |
| `payments` | Payment records |

---

## Future Improvements

- JWT authentication & role-based access
- Pagination on list endpoints
- Async MongoDB driver (Motor)
- CI/CD pipeline (GitHub Actions)
- Docker + docker-compose setup
- Rate limiting middleware
