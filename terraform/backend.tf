resource "aws_s3_bucket" "terraform_state" {
  bucket = "tmcinally-aws-remote-tfstate"

  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "tmcinally-aws-remote-tfstate-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

terraform {
  backend "s3" {
    bucket = "tmcinally-aws-remote-tfstate"
    key    = "global/s3/terraform.tfstate"
    region = "eu-west-2"

    dynamodb_table = "tmcinally-aws-remote-tfstate-locks"
    encrypt        = true
  }
}
