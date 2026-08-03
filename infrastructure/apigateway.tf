resource "aws_apigatewayv2_api" "ecom_api" {
  name          = "ecom-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "v1" {
  api_id      = aws_apigatewayv2_api.ecom_api.id
  name        = "$default"
  auto_deploy = true
}

# --- Auth Service Route ---
resource "aws_apigatewayv2_integration" "auth_integration" {
  api_id           = aws_apigatewayv2_api.ecom_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.auth_service.invoke_arn
}
resource "aws_apigatewayv2_route" "auth_route" {
  api_id    = aws_apigatewayv2_api.ecom_api.id
  route_key = "ANY /v1/auth/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.auth_integration.id}"
}
resource "aws_lambda_permission" "auth_api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.ecom_api.execution_arn}/*/*"
}

# --- Analytics Service Route ---
resource "aws_apigatewayv2_integration" "analytics_integration" {
  api_id           = aws_apigatewayv2_api.ecom_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.analytics_service.invoke_arn
}
resource "aws_apigatewayv2_route" "analytics_route" {
  api_id    = aws_apigatewayv2_api.ecom_api.id
  route_key = "ANY /v1/analytics/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.analytics_integration.id}"
}
resource "aws_lambda_permission" "analytics_api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.analytics_service.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.ecom_api.execution_arn}/*/*"
}

# Output the API URL so we can copy it to app.js
output "api_url" {
  value = aws_apigatewayv2_api.ecom_api.api_endpoint
}
