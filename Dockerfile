# Dockerfile


FROM python:3.9-alpine


WORKDIR /app

COPY requirements.txt .
COPY futuristic_city_traffic.csv .
COPY app.py .
COPY assets/ /app/assets/

# Command to run
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 8000

# 6. Define the command to run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:server"]