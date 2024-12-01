from app import app
from mangum import Mangum

# Create a handler for AWS Lambda
handler = Mangum(app)
