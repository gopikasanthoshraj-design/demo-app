# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Set the environment variable for the app to use the correct port
ENV PORT=8080

# Run the app with Gunicorn (production server)
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "app:app"]