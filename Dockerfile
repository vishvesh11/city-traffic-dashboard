# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for Dash/Plotly
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt # <-- CHANGED TO EXPLICIT PATH

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main Dash application file
COPY dashboard.py /app/dashboard.py # <-- CHANGED TO EXPLICIT PATH

# Copy the assets directory if it exists and contains your custom.css
COPY assets/ /app/assets/ # <-- CHANGED TO EXPLICIT PATH (destination must be a directory)

# Expose the port your Dash app runs on
EXPOSE 8050

# Run the Dash app when the container launches
CMD ["python", "dashboard.py"]