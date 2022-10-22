terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
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
resource "aws_ssm_parameter" "kraken-dca-eth-amount" {
  name  = "kraken-dca-ETH-daily-purchase-amount"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "kraken-dca-ada-amount" {
  name  = "kraken-dca-ADA-daily-purchase-amount"
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


resource "aws_s3_bucket" "dca-script-bucket" {
  bucket = "dca-script-bucket"
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



resource "aws_lambda_layer_version" "kraken_dca_dependencies" {
  filename   = "layer.zip"
  layer_name = "kraken_dca_dependencies"
}


resource "aws_lambda_function" "btc-dca-lambda" {
  function_name = "btc-dca-lambda"

  filename = "python_code.zip"
  
  runtime = "python3.8"
  handler = "btc_dca_script.lambda_handler"

  layers = [aws_lambda_layer_version.kraken_dca_dependencies.arn]

  role = aws_iam_role.iam-for-lambda.arn
}
