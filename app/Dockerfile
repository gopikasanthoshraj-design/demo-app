# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Firebase service account file
# IMPORTANT: Replace 'path/to/your/firebase-service-account.json' with the actual path
# or ensure the file is copied into the /app directory during build.
# For security, do not embed sensitive credentials directly in the Dockerfile.
# Consider mounting it as a secret or volume in production.
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-service-account.json

# Run app.py when the container launches
CMD ["python", "app.py"]
