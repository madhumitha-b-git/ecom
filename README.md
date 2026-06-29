# E-Commerce Backend API

A production-ready REST API built with **FastAPI** and **MongoDB**, following clean architecture principles.
Designed for internship evaluation and GitHub portfolio presentation.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Folder Structure](#folder-structure)
6. [Installation](#installation)
7. [Environment Variables](#environment-variables)
8. [Running the API](#running-the-api)
9. [Request & Response Flow](#request--response-flow)
10. [Services](#services)
11. [API Documentation](#api-documentation)
12. [HTTP Request Examples](#http-request-examples)
13. [Error Handling](#error-handling)
14. [Logging](#logging)
15. [Testing](#testing)
16. [MongoDB Collections](#mongodb-collections)
17. [Future Improvements](#future-improvements)

---

## Project Overview

This is a modular, production-ready e-commerce backend built using **FastAPI** and **MongoDB**.
It handles the core operations of an online store:

- Managing products
- Tracking inventory stock
- User shopping cart
- Order placement with stock validation
- Payment processing

The codebase follows clean architecture — routes, services, models, and database layers are fully separated.

---

## Features

- Full product catalogue CRUD (Create, Read, Update, Delete)
- Inventory management with stock tracking
- Shopping cart per user
- Order placement with automatic stock decrement
- Payment processing with SUCCESS status
- Centralized error handling with meaningful HTTP status codes
- Structured logging across all layers
- Swagger UI and ReDoc documentation
- Fully mocked unit test suite (no live DB needed for tests)
- Environment-based configuration using `.env`

---

## Tech Stack

| Layer        | Technology            |
|--------------|-----------------------|
| Framework    | FastAPI 0.111         |
| Database     | MongoDB (pymongo)     |
| Validation   | Pydantic v2           |
| Config       | pydantic-settings     |
| Testing      | pytest + httpx        |
| Server       | Uvicorn               |
| Language     | Python 3.11+          |

---

## Architecture

```
HTTP Request
     │
     ▼
 [Route Layer]          → Validates HTTP input, calls service
     │
     ▼
 [Service Layer]        → Business logic (stock check, payment, etc.)
     │
     ▼
 [Database Layer]       → MongoDB collection accessors (singleton client)
     │
     ▼
 [MongoDB Atlas]        → Persistent storage
```

- **Routes** — HTTP interface only, no business logic
- **Services** — All business logic, no HTTP concerns
- **Models** — Pydantic schemas for request validation
- **Database** — Single MongoClient singleton injected via FastAPI `Depends`
- **Exceptions** — Custom error classes with global exception handlers
- **Logger** — Shared logger factory used across all layers
- **Config** — All settings loaded from `.env` via pydantic-settings

---

## Folder Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── product_routes.py       # GET/POST/PUT/DELETE /products
│   │       ├── inventory_routes.py     # GET/POST/PUT /inventory
│   │       ├── cart_routes.py          # GET/POST/DELETE /cart
│   │       ├── payment_routes.py       # GET/POST /payments
│   │       └── order_routes.py         # GET/POST /orders
│   │
│   ├── models/
│   │   ├── product.py                  # Product Pydantic model
│   │   ├── inventory.py                # Inventory Pydantic model
│   │   ├── cart.py                     # Cart Pydantic model
│   │   ├── payment.py                  # Payment Pydantic model
│   │   └── order.py                    # Order Pydantic model
│   │
│   ├── services/
│   │   ├── product_service.py          # Product CRUD logic
│   │   ├── inventory_service.py        # Inventory logic
│   │   ├── cart_service.py             # Cart logic
│   │   ├── payment_service.py          # Payment logic
│   │   └── order_service.py            # Order orchestration logic
│   │
│   ├── database/
│   │   ├── connection.py               # Singleton MongoClient
│   │   └── mongodb.py                  # Collection accessor functions
│   │
│   ├── config.py                       # Settings from .env
│   ├── dependencies.py                 # FastAPI Depends callables
│   ├── exceptions.py                   # Custom exceptions + handlers
│   ├── logger.py                       # Shared logger factory
│   └── main.py                         # App factory + middleware
│
├── tests/
│   ├── conftest.py                     # Shared fixtures + mocked collections
│   ├── test_products.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_payment.py
│   └── test_orders.py
│
├── .env                                # Environment variables
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/madhumitha-b-git/ecom-backend.git
cd ecom-backend/backend
```

### Step 2: Create a virtual environment
```bash
python -m venv venv
```

### Step 3: Activate virtual environment

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
venv\Scripts\activate
```

**Without activating (use full path):**
```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=ecommerce_db
SECRET_KEY=your-strong-secret-key
DEBUG=false
```

| Variable       | Description                        | Default       |
|----------------|------------------------------------|---------------|
| MONGODB_URI    | MongoDB Atlas connection string    | required      |
| DATABASE_NAME  | Name of the MongoDB database       | ecommerce_db  |
| SECRET_KEY     | App secret key                     | changeme      |
| DEBUG          | Enable debug mode                  | false         |

---

## Running the API

### With venv activated:
```bash
uvicorn app.main:app --reload
```

### Without activating venv (Windows):
```powershell
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### URLs:
| Page         | URL                              |
|--------------|----------------------------------|
| API Base     | http://127.0.0.1:8000            |
| Swagger UI   | http://127.0.0.1:8000/docs       |
| ReDoc        | http://127.0.0.1:8000/redoc      |
| Health Check | http://127.0.0.1:8000/           |

---

## Request & Response Flow

### Example: Placing an Order

```
POST /orders
     │
     ▼
order_routes.py          → Receives Order model, injects 3 collections via Depends
     │
     ▼
order_service.py
  ├── 1. Find inventory by product_id       → InventoryNotFoundError (404) if missing
  ├── 2. Check stock >= quantity            → OutOfStockError (400) if insufficient
  ├── 3. Insert payment record (SUCCESS)    → payments collection
  ├── 4. Decrement inventory stock          → inventory collection
  └── 5. Insert order with status=PLACED   → orders collection
     │
     ▼
Returns: { "message": "Order Created", "order_id": "<id>" }
```

### Example: Creating a Product

```
POST /products
     │
     ▼
product_routes.py        → Validates Product model via Pydantic
     │
     ▼
product_service.py       → Inserts into products collection, logs the action
     │
     ▼
Returns: { "message": "Product Created", "product_id": "<id>" }
```

---

## Services

### product_service.py
| Function         | Description                              |
|------------------|------------------------------------------|
| create_product   | Insert a new product into MongoDB        |
| get_products     | Fetch all products                       |
| get_product      | Fetch single product by ObjectId         |
| update_product   | Update all fields of a product by ID     |
| delete_product   | Delete a product by ID                   |

### inventory_service.py
| Function          | Description                             |
|-------------------|-----------------------------------------|
| add_inventory     | Create inventory record for a product   |
| get_inventory     | Get stock level by product_id           |
| update_inventory  | Set new stock quantity for a product    |

### cart_service.py
| Function          | Description                             |
|-------------------|-----------------------------------------|
| add_to_cart       | Add a product item to user's cart       |
| get_cart          | Get all cart items for a user           |
| delete_cart_item  | Remove a specific cart item by ID       |

### payment_service.py
| Function          | Description                             |
|-------------------|-----------------------------------------|
| create_payment    | Process payment, store with SUCCESS     |
| get_payments      | Retrieve all payment records            |

### order_service.py
| Function          | Description                                          |
|-------------------|------------------------------------------------------|
| create_order      | Validate stock → process payment → place order       |
| get_orders        | Retrieve all orders                                  |
| get_order         | Retrieve single order by ObjectId                    |

---

## API Documentation

### Products

| Method | Endpoint              | Description           | Status Codes      |
|--------|-----------------------|-----------------------|-------------------|
| POST   | `/products`           | Create a product      | 201, 422          |
| GET    | `/products`           | List all products     | 200               |
| GET    | `/products/{id}`      | Get product by ID     | 200, 400, 404     |
| PUT    | `/products/{id}`      | Update product        | 200, 400, 404     |
| DELETE | `/products/{id}`      | Delete product        | 200, 400, 404     |

### Inventory

| Method | Endpoint                          | Description           | Status Codes  |
|--------|-----------------------------------|-----------------------|---------------|
| POST   | `/inventory`                      | Add inventory record  | 201, 422      |
| GET    | `/inventory/{product_id}`         | Get stock level       | 200, 404      |
| PUT    | `/inventory/{product_id}?stock=N` | Update stock          | 200, 404, 422 |

### Cart

| Method | Endpoint           | Description           | Status Codes  |
|--------|--------------------|-----------------------|---------------|
| POST   | `/cart`            | Add item to cart      | 201, 422      |
| GET    | `/cart/{user_id}`  | Get user's cart       | 200           |
| DELETE | `/cart/{cart_id}`  | Remove cart item      | 200, 400      |

### Payments

| Method | Endpoint      | Description           | Status Codes  |
|--------|---------------|-----------------------|---------------|
| POST   | `/payments`   | Process a payment     | 201, 402      |
| GET    | `/payments`   | List all payments     | 200           |

### Orders

| Method | Endpoint          | Description           | Status Codes          |
|--------|-------------------|-----------------------|-----------------------|
| POST   | `/orders`         | Place an order        | 201, 400, 402, 404    |
| GET    | `/orders`         | List all orders       | 200                   |
| GET    | `/orders/{id}`    | Get order by ID       | 200, 400, 404         |

---

## HTTP Request Examples

### Create a Product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "Noise-cancelling over-ear headphones",
    "category": "Electronics",
    "price": 89.99
  }'
```
**Response:**
```json
{ "message": "Product Created", "product_id": "64abc123def456" }
```

### Add Inventory
```bash
curl -X POST http://localhost:8000/inventory \
  -H "Content-Type: application/json" \
  -d '{ "product_id": "64abc123def456", "stock": 100 }'
```
**Response:**
```json
{ "message": "Inventory Added", "inventory_id": "64abc789xyz" }
```

### Add to Cart
```bash
curl -X POST http://localhost:8000/cart \
  -H "Content-Type: application/json" \
  -d '{ "user_id": "user1", "product_id": "64abc123def456", "quantity": 2 }'
```
**Response:**
```json
{ "message": "Added To Cart", "cart_id": "64cartid123" }
```

### Place an Order
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user1",
    "product_id": "64abc123def456",
    "quantity": 2,
    "amount": 179.98
  }'
```
**Response:**
```json
{ "message": "Order Created", "order_id": "64orderid456" }
```

### Process a Payment
```bash
curl -X POST http://localhost:8000/payments \
  -H "Content-Type: application/json" \
  -d '{ "order_id": "64orderid456", "amount": 179.98 }'
```
**Response:**
```json
{ "payment_id": "64paymentid789", "status": "SUCCESS" }
```

### Update Stock
```bash
curl -X PUT "http://localhost:8000/inventory/64abc123def456?stock=50"
```
**Response:**
```json
{ "message": "Stock Updated" }
```

---

## Error Handling

All errors return structured JSON with meaningful HTTP status codes.

| Error                  | Status Code | Response                          |
|------------------------|-------------|-----------------------------------|
| Invalid ObjectId       | 400         | `{ "detail": "Invalid ID format" }` |
| Product Not Found      | 404         | `{ "detail": "Product Not Found" }` |
| Inventory Not Found    | 404         | `{ "detail": "Inventory Not Found" }` |
| Out Of Stock           | 400         | `{ "detail": "Out Of Stock" }` |
| Empty Cart             | 400         | `{ "detail": "Cart Is Empty" }` |
| Payment Failed         | 402         | `{ "detail": "Payment Failed" }` |
| Order Not Found        | 404         | `{ "detail": "Order Not Found" }` |
| Validation Error       | 422         | Pydantic validation details |

---

## Logging

Logs are printed to stdout in this format:
```
2024-01-15 10:30:00 | INFO     | app.services.product_service | DB | Product created: 64abc123
2024-01-15 10:30:01 | INFO     | app.api.routes.order_routes  | POST /orders | user=user1
2024-01-15 10:30:01 | INFO     | app.services.order_service   | Order PLACED | order_id=64orderid456
```

Logged events:
- Every API request (method + path)
- Every API response (method + path + status code)
- Database insert / update / delete operations
- Order placement (success)
- Payment status
- MongoDB connection established
- All errors

---

## Testing

### Run all tests
```bash
# With venv activated
pytest

# Without activating venv
venv\Scripts\python.exe -m pytest
```

### Test coverage

| File                | Test Cases                                         |
|---------------------|----------------------------------------------------|
| test_products.py    | Create, Read all, Read one, Update, Delete, Invalid ID, Not Found |
| test_inventory.py   | Add, Get, Get not found, Update stock, Invalid stock, Not found |
| test_cart.py        | Add to cart, Get cart, Empty cart, Delete item, Invalid ID |
| test_payment.py     | Payment success, List payments                     |
| test_orders.py      | Place order, Out of stock, Inventory not found, Get all, Get one, Invalid ID |

All tests use `unittest.mock.MagicMock` — **no live MongoDB required**.

---

## MongoDB Collections

| Collection  | Purpose                        | Key Fields                              |
|-------------|--------------------------------|-----------------------------------------|
| products    | Product catalogue              | name, description, category, price      |
| inventory   | Stock levels per product       | product_id, stock                       |
| cart        | User cart items                | user_id, product_id, quantity           |
| orders      | Placed orders                  | user_id, product_id, quantity, amount, status |
| payments    | Payment records                | order_id, amount, status                |

---

## Future Improvements

- JWT authentication & role-based access control
- Pagination on all list endpoints
- Async MongoDB driver (Motor) for better performance
- CI/CD pipeline with GitHub Actions
- Docker + docker-compose setup
- Rate limiting middleware
- Order cancellation endpoint
- Email notifications on order placement
- Product search and filtering
- Admin dashboard
