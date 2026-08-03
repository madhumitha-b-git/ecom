# 1. Auth Service Lambda
resource "aws_lambda_function" "auth_service" {
  function_name = "auth-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30

  # We use a dummy payload just to create the infrastructure. 
  # Your deploy_to_aws.py script will upload the real code!
  filename = "dummy.zip"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.users.name
    }
  }
}

# 2. Analytics Service Lambda
resource "aws_lambda_function" "analytics_service" {
  function_name = "analytics-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30

  filename = "dummy.zip"

  environment {
    variables = {
      S3_RAW_BUCKET   = aws_s3_bucket.data_lake_raw.bucket
      S3_STAGE_BUCKET = aws_s3_bucket.data_lake_stage.bucket
    }
  }
}

# 3. Order Service Lambda
resource "aws_lambda_function" "order_service" {
  function_name = "order-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30

  filename = "dummy.zip"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
      SNS_TOPIC  = aws_sns_topic.order_events.arn
    }
  }
}

# 4. Inventory Service Lambda
resource "aws_lambda_function" "inventory_service" {
  function_name = "inventory-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30
  filename      = "dummy.zip"
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.inventory.name
    }
  }
}

# 5. Payment Service Lambda
resource "aws_lambda_function" "payment_service" {
  function_name = "payment-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30
  filename      = "dummy.zip"
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.payment.name
    }
  }
}

# 6. Cart Service Lambda
resource "aws_lambda_function" "cart_service" {
  function_name = "cart-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30
  filename      = "dummy.zip"
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.cart.name
    }
  }
}

# 7. Product Service Lambda
resource "aws_lambda_function" "product_service" {
  function_name = "product-service_ecom"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "main.handler"
  runtime       = "python3.12"
  timeout       = 30
  filename      = "dummy.zip"
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.products.name
    }
  }
}

# --- Event Source Mappings (SQS to Lambda) ---
resource "aws_lambda_event_source_mapping" "inventory_sqs_trigger" {
  event_source_arn = aws_sqs_queue.inventory_events.arn
  function_name    = aws_lambda_function.inventory_service.arn
  batch_size       = 10
}

resource "aws_lambda_event_source_mapping" "payment_sqs_trigger" {
  event_source_arn = aws_sqs_queue.payment_events.arn
  function_name    = aws_lambda_function.payment_service.arn
  batch_size       = 10
}

