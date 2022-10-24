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