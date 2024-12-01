#!/bin/bash

# Variables
FUNCTION_NAME="unit-conversion-api"
ZIP_FILE="deployment_package.zip"
REGION="us-east-1"
ROLE_ARN="arn:aws:iam::132667624413:role/LambdaExecutionRole" 

# Clean up old deployment files
rm -f $ZIP_FILE

# Install dependencies and package the app
pip install -r requirements.txt -t ./package
cp -r src/* package/
cp scripts/lambda_handler.py package/
cd package
zip -r ../$ZIP_FILE .
cd ..

# Create or update the Lambda function
aws lambda get-function --function-name $FUNCTION_NAME --region $REGION &> /dev/null
if [ $? -ne 0 ]; then
    echo "Creating a new Lambda function..."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime python3.9 \
        --role $ROLE_ARN \
        --handler scripts.lambda_handler.handler \
        --timeout 10 \
        --memory-size 128 \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
else
    echo "Updating the existing Lambda function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
fi
