resource "aws_cloudwatch_event_rule" "kraken_dca_lambda_event_rule" {
  name = "kraken_dca_lambda_event_rule"
  description = "execute event every day at 10:00 UTC"
  schedule_expression = "cron(0 10 * * ? *)"
}

resource "aws_cloudwatch_event_target" "kraken_dca_lambda_event_target" {
  arn = aws_lambda_function.btc-dca-lambda.arn
  rule = aws_cloudwatch_event_rule.kraken_dca_lambda_event_rule.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.btc-dca-lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.kraken_dca_lambda_event_rule.arn
}