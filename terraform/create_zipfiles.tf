data "archive_file" "dependencies_zip" {
  type = "zip"

  source_dir  = "./${path.module}/../dependencies"
  output_path = "./${path.module}/layer.zip"
}

data "archive_file" "source_code_zip" {
  type = "zip"

  source_file  = "./${path.module}/../btc_dca_script.py"
  output_path = "./${path.module}/python_code.zip"
}