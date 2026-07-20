# Frontend-Backend Integration Guide

This guide describes how to connect the E-Commerce HTML/JS frontend to your FastAPI microservice backend and verify your application.

---

## 1. Gateway & Endpoint Settings

The frontend includes a **Settings Panel** (accessible via the Gear icon <i class="fa-solid fa-cog"></i> in the bottom-left corner of the browser) where you can switch the Execution Mode:
- **Simulated / Mock Mode**: Runs the frontend completely offline using mock data, order placement simulation, and live state updates. Perfect for standalone demonstrations.
- **Live API Gateway Mode**: Forwards all requests (Product, Cart, Order, Inventory, Payment) to local or AWS-hosted FastAPI endpoints.

By default, the following ports are configured for local FastAPI services:
- **Order Service**: `http://localhost:8000`
- **Cart Service**: `http://localhost:8001`
- **Inventory Service**: `http://localhost:8002`
- **Payment Service**: `http://localhost:8003`
- **Product Service**: `http://localhost:8004`

---

## 2. API Endpoints Map

The frontend JavaScript [app.js](file:///c:/Users/madhumitha.b/OneDrive%20-%20IDP%20Education%20Ltd/Desktop/ECOM/frontend/app.js) communicates with your microservices using standard REST calls:

### Product Service (`/products`)
- **List Products**: `GET /products`
  - Expected Response: A JSON list of products:
    ```json
    [
      {
        "product_id": "prod-1",
        "name": "Floral Dress",
        "description": "Red floral print cotton dress",
        "price": 49.99,
        "category": "Dresses",
        "image": "https://..."
      }
    ]
    ```
- **Create Product**: `POST /products`
  - Body payload:
    ```json
    {
      "name": "Classic Jeans",
      "description": "Blue denim classic fit jeans",
      "price": 89.99,
      "category": "Footwear",
      "image": "https://..."
    }
    ```
- **Delete Product**: `DELETE /products/{id}`

### Inventory Service (`/inventory`)
- **Update Stock**: `PUT /inventory/{product_id}?stock={qty}`
- **Decrement Stock (called after order placement)**: `POST /inventory/{product_id}/decrement?quantity={qty}`

### Order Service (`/orders`)
- **Place Order**: `POST /orders`
  - Body payload:
    ```json
    {
      "user_id": "user123",
      "product_id": "prod-1",
      "quantity": 2,
      "amount": 99.98,
      "size": "M"
    }
    ```

### Payment Service (`/payments`)
- **Process Transaction**: `POST /payments`
  - Body payload:
    ```json
    {
      "order_id": "order-123456",
      "amount": 99.98
    }
    ```

---

## 3. How to Run Locally

### Step A: Run the Backend Services
Make sure your FastAPI services are started on their respective ports. For example, to start the Product Service:
```bash
cd microservices/product-service
python -m uvicorn main:app --port 8004 --reload
```
Repeat for each service (ports 8000-8003).

### Step B: Open the Frontend
Since the frontend consists of pure HTML/JS/CSS, you can run it directly:
1. Double-click the [index.html](file:///c:/Users/madhumitha.b/OneDrive%20-%20IDP%20Education%20Ltd/Desktop/ECOM/frontend/index.html) file to open it in any web browser.
2. Alternatively, serve it locally using Python's built-in HTTP server:
   ```bash
   cd frontend
   python -m http-server 8080
   ```
   Then open `http://localhost:8080` in your browser.

### Step C: Configure and Verify
1. Click the **Gear icon** in the bottom-left corner of the frontend interface.
2. Switch to **Live API endpoints**.
3. Verify or update the port URLs to match your running backend services.
4. Click **Save configurations**.
5. Add items to the cart, select sizes, and complete transactions to verify that order data and inventory levels update dynamically in your backend DynamoDB tables.
