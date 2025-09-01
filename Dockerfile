# Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn

# Copy the rest 
COPY . .

# Flask settings
ENV PYTHONPATH=/app

# Expose Flask’s default port
EXPOSE 5000

# Start the server (flask run)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "model_training:app"]