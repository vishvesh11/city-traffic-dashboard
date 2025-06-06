# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for Dash/Plotly (e.g., for some fonts or libraries)
# Removed git as it's likely not needed for runtime, keeping build-essential and curl for general utility
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main Dash application file
COPY dashboard.py . # Corrected: from app.py to dashboard.py

# Copy the assets directory if it exists and contains your custom.css
COPY assets/ ./assets/

# Expose the port your Dash app runs on
EXPOSE 8050

# Run the Dash app when the container launches
CMD ["python", "dashboard.py"]