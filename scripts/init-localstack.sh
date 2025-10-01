#!/bin/bash

echo "Waiting for LocalStack to be ready..."
until curl -s http://localhost:4566/_localstack/health | grep -q '"sqs": "available"' && curl -s http://localhost:4566/_localstack/health | grep -q '"ses": "available"'; do
  echo "Waiting for SQS and SES services..."
  sleep 2
done

echo "Creating SQS queue: celery"
awslocal sqs create-queue --queue-name celery

echo "Verifying SES email identity: test@test.com"
awslocal ses verify-email-identity --email-address test@test.com --region ${SQS_REGION:-us-east-1}

echo "LocalStack initialization completed successfully!"
echo "- SQS queue 'celery' created"
echo "- SES email 'test@test.com' verified"
