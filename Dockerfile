# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for Dash/Plotly
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your main Dash application file
COPY dashboard.py /app/dashboard.py
COPY futuristic_city_traffic.csv /app/futuristic_city_traffic.csv

COPY assets/ /app/assets/

# Expose the port your Dash app runs on
EXPOSE 8050

# Run the Dash app when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8050", "dashboard:server"]