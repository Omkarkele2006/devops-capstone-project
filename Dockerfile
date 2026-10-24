FROM python:3.9-slim

# Create working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY service/ ./service/

# Create non-root user for security
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose application port
EXPOSE 8080

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "service:app"]
