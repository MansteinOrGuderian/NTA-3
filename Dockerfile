# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the lab3.py file into the container
COPY lab3.py .

# Specify the command to run the application
CMD ["python", "lab3.py"]

