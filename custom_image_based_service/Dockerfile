# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install necessary dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
