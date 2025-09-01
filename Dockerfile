FROM python:3.11-slim

# Set up environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir inside the container
WORKDIR /app

# Install Python dependicies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest
COPY . .

# Flask dev server will listen on 5000
EXPOSE 5000

# Start the app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "iris-species-prediction-app.py"]
