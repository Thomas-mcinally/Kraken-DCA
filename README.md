# Kraken-DCA
- Serverless application that automates recurring purchases of crypto on Kraken Exchange
  - Works for any cryptocurrency available on Kraken, and any desired purchase interval
- Made so that it is easy for you to **run in your own AWS account**, using the AWS free tier 
- 90% reduction in trading fees as compared to using the built-in recurring purchase feature in the Kraken mobile app


## AWS Infrastructure
- AWS Lambda holds python script and dependencies
- AWS Eventbridge used to schedule Lambda function execution
- AWS SSM used to store API keys and purchase budget, accessed from Lambda function
- AWS S3 bucket used to store Terraform remote state (enables CI/CD pipeline)
- NAT instance has constant IP address (enables IP whitelisting for API keys)
- Use NAT instance instead of NAT gateway because it is much cheaper and within AWS free tier



![](diagrams/aws_infra.png)

