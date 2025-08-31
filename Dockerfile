# Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Flask app code
COPY . .

# Flask settings
ENV FLASK_APP=ham_spam_app.py:app \
    FLASK_RUN_HOST=0.0.0.0

# Expose Flask’s default port
EXPOSE 5000

# Start the server (flask run)

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "ham_spam_app:app"]