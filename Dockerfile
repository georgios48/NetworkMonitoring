# Use an official Python runtime as a parent image
FROM python:3.11.1

# Set the working directory inside the container
WORKDIR /app

# Copy only the Backend folder into the container
COPY Backend /app

# Ensure /app/templates is writable by all users
RUN chmod -R 777 /app/templates

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8001 8050 62079

# Run Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "app.py"]