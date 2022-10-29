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

resource "aws_lambda_function" "btc-withdraw-lambda" {
  function_name = "btc-withdraw-lambda"

  filename = "btc_withdraw_python_code.zip"

  runtime = "python3.8"
  handler = "withdraw.lambda_handler"

  layers = [aws_lambda_layer_version.kraken_dca_dependencies.arn]

  source_code_hash = data.archive_file.withdraw_source_code_zip.output_base64sha256

  role = aws_iam_role.iam-for-lambda.arn
}