# Use an official Python runtime as a parent image
FROM python:3.11.1

# Set the working directory inside the container
WORKDIR /app

# Copy only the Backend folder into the container
COPY Backend /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on (change if needed)
EXPOSE 8001

# Run Flask app
CMD ["python", "app.py"]