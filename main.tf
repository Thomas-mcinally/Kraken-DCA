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