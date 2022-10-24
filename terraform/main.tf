terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.36.1"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_ssm_parameter" "kraken-dca-btc-amount" {
  name  = "kraken-dca-BTC-daily-purchase-amount"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "kraken-public-api-key" {
  name  = "kraken-public-api-key"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "kraken-private-api-key" {
  name  = "kraken-private-api-key"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}


resource "aws_iam_role" "iam-for-lambda" {
  name = "iam-for-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "kraken_dca_lambda_policy" {
  role       = aws_iam_role.iam-for-lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
resource "aws_iam_role_policy_attachment" "kraken_dca_lambda_access_to_ssm" {
  role       = aws_iam_role.iam-for-lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}


data "archive_file" "dependencies_zip" {
  type = "zip"

  source_dir  = "./${path.module}/../dependencies"
  output_path = "./${path.module}/../layer.zip"
}

data "archive_file" "source_code_zip" {
  type = "zip"

  source_file  = "./${path.module}/../btc_dca_script.py"
  output_path = "./${path.module}/../python_code.zip"
}

resource "aws_lambda_layer_version" "kraken_dca_dependencies" {
  filename   = "layer.zip"
  layer_name = "kraken_dca_dependencies"

  source_code_hash = data.archive_file.dependencies_zip.output_base64sha256
}


resource "aws_lambda_function" "btc-dca-lambda" {
  function_name = "btc-dca-lambda"

  filename = "python_code.zip"

  runtime = "python3.8"
  handler = "btc_dca_script.lambda_handler"

  layers = [aws_lambda_layer_version.kraken_dca_dependencies.arn]

  source_code_hash = data.archive_file.source_code_zip.output_base64sha256

  role = aws_iam_role.iam-for-lambda.arn
}

resource "aws_cloudwatch_event_rule" "kraken_dca_lambda_event_rule" {
  name = "kraken_dca_lambda_event_rule"
  description = "execute event every day at 10:00 UTC"
  schedule_expression = "cron(0 10 * * ? *)"
}

resource "aws_cloudwatch_event_target" "kraken_dca_lambda_event_target" {
  arn = aws_lambda_function.btc-dca-lambda.arn
  rule = aws_cloudwatch_event_rule.kraken_dca_lambda_event_rule.name
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_rw_fallout_retry_step_deletion_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.btc-dca-lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.kraken_dca_lambda_event_rule.arn
}