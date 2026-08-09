# ShopEase E-Commerce Platform - Serverless Microservices Architecture 🚀

A production-grade, event-driven, serverless e-commerce microservices platform built with Vanilla JS, Python, AWS Lambda, Amazon DynamoDB, Amazon API Gateway, Amazon SNS & SQS, Terraform (IaC), and continuous integration via GitHub Actions and SonarCloud.

---

## 🌟 Executive Summary & Key Highlights

*   **Architecture:** 7 decoupled, highly-scalable microservices running on AWS Lambda, fronted by Amazon API Gateway.
*   **Database Layer:** High-performance NoSQL with 6 Amazon DynamoDB tables utilizing partition key schemas optimized for rapid querying.
*   **Authentication:** Centralized custom JWT (JSON Web Token) authentication verifying user sessions securely.
*   **Event-Driven Messaging:** Asynchronous, decoupled event publishing and consumption via Amazon SNS (`order-event`, `inventory-result`) and dedicated SQS queues (`inventory-events`, `payment-events`).
*   **Infrastructure as Code (IaC):** Modular Terraform configuration managing DynamoDB, Lambda, IAM permissions, API Gateway, SNS/SQS, and an S3 Data Lake.
*   **Data Lake Integration:** Raw and Staging Amazon S3 buckets (`ecom-data-lake-raw`, `ecom-data-lake-stage`) provisioned for advanced analytics.
*   **CI/CD & Security:** Automated GitHub Actions pipelines for every microservice, integrating automated testing and SonarCloud Quality Gate compliance for robust CI/CD.

---

## 🔗 Live URLs (For Mentor Evaluation)

*   **GitHub Repository:** [https://github.com/madhumitha-b-git/ecom](https://github.com/madhumitha-b-git/ecom)
*   **CloudFront Live URL:** https://d1r2j7yy09n0mr.cloudfront.net/ 

---

## 🧩 Microservices Specification (7 Backend Services)

| Microservice | Primary Responsibility | DynamoDB Table Name | Partition Key |
| :--- | :--- | :--- | :--- |
| **`auth-service`** | Profile registration, login, and JWT token issuance | `ecom-users` | `email` (S) |
| **`product-service`** | Product catalog management | `Products_ecom` | `product_id` (S) |
| **`inventory-service`** | Stock reservation & real-time inventory updates | `inventory_ecom` | `product_id` (S) |
| **`cart-service`** | Cart management & subtotal calculations | `cart_ecom` | `cart_id` (S) |
| **`order-service`** | Order placement & fulfillment tracking | `orders_ecom` | `order_id` (S) |
| **`payment-service`** | Secure payment transaction processing | `payment_ecom` | `payment_id` (S) |
| **`analytics-service`** | System metrics tracking & business reporting | *N/A (Data Lake)* | — |

---

## 📬 Event-Driven Architecture (SNS & SQS)

The application utilizes an asynchronous publish/subscribe model to strictly decouple order creation, inventory allocation, and payment processing:

*   **Order Placed Workflow:**
    *   **SNS Topic:** `order-event_ecom` is published when a new order is initialized.
    *   **SQS Queue:** `inventory-event_ecom` subscribes to this topic and triggers the inventory service to safely allocate stock.
*   **Payment Processing Workflow:**
    *   **SNS Topic:** `inventory-result_ecom` is published once stock is successfully allocated.
    *   **SQS Queue:** `payment-event_ecom` subscribes to this topic and finalizes the financial transaction.

---

## 🛠️ Infrastructure as Code (Terraform)

All AWS cloud infrastructure is declaratively managed under the `/infrastructure` directory to ensure reproducible and reliable deployments.

```text
/infrastructure
├── main.tf                 # Provider configurations
├── apigateway.tf           # AWS API Gateway configuration mapping to Lambda
├── lambda.tf               # Lambda function provisioning and zip deployments
├── dynamodb.tf             # 6 DynamoDB production table resources
├── sns.tf                  # SNS topics for event broadcasting
├── sqs.tf                  # SQS queues and access policies
├── s3.tf                   # S3 Data Lake (Raw and Stage buckets)
└── iam.tf                  # Principle of Least Privilege execution roles
```

---

## 💻 Frontend Design & Functionality

The frontend application (`/frontend`) is built utilizing cutting-edge web design principles:

*   **Premium Glassmorphism Aesthetics:** A sleek, modern UI utilizing deep contrast, responsive CSS variables, and dynamic hover micro-animations.
*   **Admin Dashboard:** A real-time, comprehensive view of product inventory, live payment ledgers, and revenue analytics. Includes intelligent client-side deduplication.
*   **Report Generation:** Built-in PDF report generation using `jsPDF` for instant receipt downloads.
*   **Live Notifications:** Dynamic notification bell system alerting the admin of low stock scenarios and real-time interactions.

---

## 🚀 CI/CD Pipelines (GitHub Actions)

*   **Service-Level Pipelines:** Individual GitHub Actions workflows (`.github/workflows/`) for each microservice (`auth-service.yml`, `order-service.yml`, etc.).
*   **Validation:** Executes automated CI validation prior to merging.

---

## 🔒 Security, Compliance & Observability

*   **Snyk Vulnerability Auditing:** Automated SAST security testing is integrated into the CI pipelines. The repository currently maintains a flawless security posture with **0 Critical Vulnerabilities** across all 7 microservices.
*   **SonarCloud Quality Gate:** Pre-configured Quality Profiles enforce strict testing boundaries, achieving a green PASSED Quality Gate rating for code maintainability and reliability.
*   **AWS X-Ray Distributed Tracing:** Full distributed request tracing is enabled across API Gateway and Lambda functions to pinpoint latency and trace asynchronous events traversing through SNS and SQS.
*   **AWS CloudWatch Dashboards:** A unified CloudWatch Dashboard provides deep observability into Invocations, Errors, Latency, and Throttling metrics for all microservices in real-time.

---

## 🏃 Local Setup & Testing Commands

### Prerequisites
*   Node.js & Python installed
*   Terraform v1.5+
*   AWS CLI configured (`aws sso login`)

### Running the Project Locally

**1. Deploy Infrastructure**
```bash
cd infrastructure
terraform init
terraform apply -auto-approve
```

**2. Start the Frontend Application**
```bash
python -m http.server 8000                           
```
*(Open the provided localhost URL in your browser)*

---

## 👨‍💻 Project Maintainer
**Developer:** Madhumitha
**Repository:** [https://github.com/madhumitha-b-git/ecom](https://github.com/madhumitha-b-git/ecom)
