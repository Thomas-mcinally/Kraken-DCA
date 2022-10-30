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
resource "aws_ssm_parameter" "XXBT-hardwallet" {
  name  = "XXBT-hardwallet"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "XETH-hardwallet" {
  name  = "XETH-hardwallet"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "kraken-public-withdraw-api-key" {
  name  = "kraken-public-withdraw-api-key"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}
resource "aws_ssm_parameter" "kraken-private-withdraw-api-key" {
  name  = "kraken-private-withdraw-api-key"
  type  = "SecureString"
  value = "SET MANUALLY IN AWS CONSOLE"
  lifecycle {
    ignore_changes = [value]
  }
}