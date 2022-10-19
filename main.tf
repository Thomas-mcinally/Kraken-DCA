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

resource "aws_s3_bucket" "dca-script-bucket" {
  bucket = "dca-script-bucket"
}



# resource "aws_iam_role" "iam-for-lambda" {
#   name = "iam-for-lambda"

#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": "sts:AssumeRole",
#       "Principal": {
#         "Service": "lambda.amazonaws.com"
#       },
#       "Effect": "Allow",
#       "Sid": ""
#     }
#   ]
# }
# EOF
# }

# resource "aws_lambda_function" "btc-dca-lambda" {
#   function_name = "btc-dca-lambda"

#   s3_bucket = aws_s3_bucket.dca-script-bucket.id
#   s3_key = "btc_dca_script.zip"
  
#   runtime = "python3.8"
#   handler = "btc_dca_script.lambda_handler"

#   source_code_hash = filebase64sha256("btc_dca_script.zip")

#   role = aws_iam_role.iam-for-lambda.arn

#   # environment {
#   #   variables = {
#   #     foo = "bar"
#   #   }
#   # }
# }
