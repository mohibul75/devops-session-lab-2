# Microservices App

A simple microservices application with two FastAPI services and Nginx as a reverse proxy.

## Architecture

- **Service 1**: A simple FastAPI service that manages items
- **Service 2**: A simple FastAPI service that manages tasks and can communicate with Service 1
- **Nginx**: Acts as a reverse proxy to route traffic to the appropriate service

## Prerequisites

- Docker and Docker Compose
- Python 3.11 (for local development)
- AWS account with ECR repositories (for deployment)

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd microservices-app
```

2. Install dependencies for local development:
```bash
cd microservices/service1
pip install -r requirements.txt
cd ../service2
pip install -r requirements.txt
```

3. Run the services locally:
```bash
cd microservices/service1
python main.py
# In another terminal
cd microservices/service2
python main.py
```

## Running with Docker Compose

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Access the services:
   - Service 1: http://localhost/service1
   - Service 2: http://localhost/service2

3. Stop the containers:
```bash
docker-compose down
```

## Testing

Run tests for each service:
```bash
cd microservices/service1
pytest
cd ../service2
pytest
```

## CI/CD Pipeline

The application includes a GitHub Actions workflow that:
1. Runs tests for both services
2. Builds Docker images
3. Pushes images to Amazon ECR
4. Deploys to EC2 instance

### Setting up AWS OIDC for GitHub Actions

This project uses OpenID Connect (OIDC) for secure authentication with AWS. To set up:

1. Create an IAM role in your AWS account with the following trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>:*"
        }
      }
    }
  ]
}
```

2. Attach policies to the IAM role that provide permissions for ECR and any other AWS services you need.

3. Configure the OIDC provider in AWS IAM:
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

### Required GitHub Secrets

To use the CI/CD pipeline, add these secrets to your GitHub repository:

- `AWS_ROLE_TO_ASSUME`: ARN of the IAM role created for OIDC (e.g., `arn:aws:iam::123456789012:role/GitHubActionsOIDC`)
- `AWS_REGION`: AWS region (e.g., `us-east-1`)
- `AWS_ACCOUNT_ID`: Your AWS account ID
- `EC2_HOST`: EC2 instance public IP or DNS
- `EC2_USERNAME`: SSH username (e.g., `ec2-user`)
- `EC2_SSH_KEY`: SSH private key for EC2 access

## API Documentation

After starting the services, access the Swagger UI documentation:
- Service 1: http://localhost/service1/docs
- Service 2: http://localhost/service2/docs 