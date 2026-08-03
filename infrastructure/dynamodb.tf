# Auth Service Table
resource "aws_dynamodb_table" "users" {
  name           = "ecom-users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }
}

# Order Service Table
resource "aws_dynamodb_table" "orders" {
  name           = "orders_ecom"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

# Inventory Service Table
resource "aws_dynamodb_table" "inventory" {
  name           = "inventory_ecom"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product_id"

  attribute {
    name = "product_id"
    type = "S"
  }
}

# Product Service Table
resource "aws_dynamodb_table" "products" {
  name           = "Products_ecom"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product_id"

  attribute {
    name = "product_id"
    type = "S"
  }
}

# Cart Service Table
resource "aws_dynamodb_table" "cart" {
  name           = "cart_ecom"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "cart_id"

  attribute {
    name = "cart_id"
    type = "S"
  }
}

# Payment Service Table
resource "aws_dynamodb_table" "payment" {
  name           = "payment_ecom"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "payment_id"

  attribute {
    name = "payment_id"
    type = "S"
  }
}
