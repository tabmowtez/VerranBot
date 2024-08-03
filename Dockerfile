# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Update o/s packages
RUN apt-get update && apt-get -y upgrade

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy the rest of the application code into the container
COPY . .

# Run the bot when the container launches
CMD ["python", "bot.py"]
