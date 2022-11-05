data "archive_file" "dependencies_zip" {
  type = "zip"

  source_dir  = "./${path.module}/../dependencies"
  output_path = "./${path.module}/layer.zip"
}

data "archive_file" "source_code_zip" {
  type = "zip"

  source_file = "./${path.module}/../python_scripts/dca.py"
  output_path = "./${path.module}/python_code.zip"
}

data "archive_file" "withdraw_source_code_zip" {
  type = "zip"

  source_file = "./${path.module}/../python_scripts/withdraw.py"
  output_path = "./${path.module}/kraken_withdraw_python_code.zip"
}