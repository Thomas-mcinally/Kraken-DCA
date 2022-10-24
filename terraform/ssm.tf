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