# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Cloud Run
ENV PORT=8080

# Expose the port the app runs on
EXPOSE 8080

# Run the app with Gunicorn as the entry point
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "app:app"]