# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Create logs directory
RUN mkdir -p /app/logs

# Install curl
RUN apt-get update && apt-get install -y curl

# Set PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "src/app.py"]
