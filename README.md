# Kraken-DCA
- This project is used to automatically buy a set amount of BTC daily, using Kraken exchange API endpoints
  - Can modify to work for any cryptocurrency or any purchase interval
- 90% reduction in trading fees as compared to using the built-in recurring purchase feature in the Kraken mobile app

## Design
- AWS architecture: 
  - AWS Lambda holds python script
  - AWS Eventbridge used to schedule Lambda function execution
  - AWS SSM used to store API keys and purchase amount, accessed from lambda function
  - AWS S3 bucket used to store Terraform remote state (enables CI/CD pipeline)

- CI/CD pipeline using Pytest and Terraform with Github actions
- Developed using TDD
