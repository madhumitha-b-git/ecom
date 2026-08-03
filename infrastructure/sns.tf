resource "aws_sns_topic" "order_events" {
  name = "order-event_ecom"
}

resource "aws_sns_topic" "inventory_result" {
  name = "inventory-result_ecom"
}

resource "aws_sns_topic_subscription" "order_to_inventory" {
  topic_arn = aws_sns_topic.order_events.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.inventory_events.arn
}

resource "aws_sns_topic_subscription" "inventory_to_payment" {
  topic_arn = aws_sns_topic.inventory_result.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.payment_events.arn
}
