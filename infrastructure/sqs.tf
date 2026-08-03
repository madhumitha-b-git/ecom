resource "aws_sqs_queue" "payment_events" {
  name = "payment-event_ecom"
}

resource "aws_sqs_queue" "inventory_events" {
  name = "inventory-event_ecom"
}

# Allow SNS to publish to SQS
resource "aws_sqs_queue_policy" "payment_events_policy" {
  queue_url = aws_sqs_queue.payment_events.id
  policy    = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "sqs:SendMessage"
        Resource = aws_sqs_queue.payment_events.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.inventory_result.arn
          }
        }
      }
    ]
  })
}

resource "aws_sqs_queue_policy" "inventory_events_policy" {
  queue_url = aws_sqs_queue.inventory_events.id
  policy    = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "sqs:SendMessage"
        Resource = aws_sqs_queue.inventory_events.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.order_events.arn
          }
        }
      }
    ]
  })
}
