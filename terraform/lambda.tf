resource "aws_lambda_layer_version" "kraken_dca_dependencies" {
  filename   = "layer.zip"
  layer_name = "kraken_dca_dependencies"

  source_code_hash = data.archive_file.dependencies_zip.output_base64sha256
}

resource "aws_lambda_function" "kraken-dca-lambda" {
  function_name = "kraken-dca-lambda"

  filename = "python_code.zip"

  runtime = "python3.8"
  handler = "dca.lambda_handler"

  layers = [aws_lambda_layer_version.kraken_dca_dependencies.arn]

  source_code_hash = data.archive_file.source_code_zip.output_base64sha256

  role = aws_iam_role.iam-for-lambda.arn

  timeout = 10

  vpc_config {
    subnet_ids         = [aws_subnet.private_subnet.id]
    security_group_ids = [aws_default_security_group.default_security_group_for_vpc.id]
  }

}

resource "aws_lambda_function" "kraken-withdraw-lambda" {
  function_name = "kraken-withdraw-lambda"

  filename = "kraken_withdraw_python_code.zip"

  runtime = "python3.8"
  handler = "withdraw.lambda_handler"

  layers = [aws_lambda_layer_version.kraken_dca_dependencies.arn]

  source_code_hash = data.archive_file.withdraw_source_code_zip.output_base64sha256

  role = aws_iam_role.iam-for-lambda.arn

  timeout = 10

   vpc_config {
    subnet_ids         = [aws_subnet.private_subnet.id]
    security_group_ids = [aws_default_security_group.default_security_group_for_vpc.id]
  }

}
