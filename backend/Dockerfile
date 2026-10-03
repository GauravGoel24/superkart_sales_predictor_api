
# Use Python 3.13 base image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application
COPY app.py .

# Copy serialized machine learning model
COPY superkart_sales_model.pkl .

# Expose application port
EXPOSE 5000

# Start Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:superkart_sales_predictor_api"]
