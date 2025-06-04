# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app ./app

# Set environment variables to ensure stdout and stderr are flushed immediately
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app/main.py"]
