# Unit Conversion Grading System

## Overview
This project provides a REST API for grading students' unit conversion problems. Teachers can input a numerical value, the unit to convert from, the target unit, and the student's response. The system evaluates whether the response is correct, incorrect, or invalid.

## Features
- Supports temperature conversions (Celsius, Kelvin, Fahrenheit, Rankine).
- Validates user input for correctness.
- REST API built with Flask.
- CI/CD pipeline with GitHub Actions.
- Deployed to AWS Lambda.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app locally:
   ```bash
   python src/app.py
4. Run tests:
   ```bash
   pytest tests/

## How to Run
1. With Docker:
   ```bash
   docker-compose up
2. Without Docker:
   ```bash 
   pip install -r requirements.txt
   python src/app.py

## How to Test API
1. In the terminal Run:
   ```bash
   curl -X POST http://localhost:8080/convert \
   -H "Content-Type: application/json" \
   -d '{
         "value": 84.2,
         "from_unit": "fahrenheit",
         "to_unit": "rankine",
         "student_response": 543.9
      }'
   ```
- Expected output:
   ```json
   {"output": "correct"}
   ```

2. With a tool like postman, create a `POST` request to "http://127.0.0.1:8080/convert" . 
In the body of the request, use
   ```json 
   {
        "value": 317.33,
        "from_unit": "kelvin",
        "to_unit": "fahrenheit",
        "student_response": 111.56
    }
    ```
- Expected output:
   ```json
   {"output": "incorrect"}
   ```

## Deployment
### Automated Deployment
Deployment is automated via GitHub Actions. On merging to the main branch, the application is deployed to AWS Lambda.

### Manual Deployment
1. Ensure you have the AWS CLI configured with appropriate credentials.
2. Execute the deploy_to_lambda.sh script:
   ```bash
   bash scripts/deploy_to_lambda.sh


## Improvements
1. Add support for other unit types (e.g., distance, weight).
2. Implement a user-friendly frontend for teacher interactions.
3. Enhance validation for input edge cases.
4. Optimize performance for large datasets.
5. Integrate with a database for storing results and configurations.