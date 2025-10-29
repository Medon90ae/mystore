# Stage 1: Build stage to install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install poetry for dependency management
RUN pip install poetry

# Copy only dependency definition files
COPY poetry.lock pyproject.toml ./

# Install dependencies without creating a virtualenv in the image
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Stage 2: Final image
FROM python:3.11-slim AS final

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY ./app ./app
COPY pyproject.toml poetry.lock ./

# Set environment variables for Gunicorn (default port 8080 if not set)
ENV PORT=8080
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:${PORT} --workers=1 --worker-class=uvicorn.workers.UvicornWorker --log-level=info"

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "app.main:app"]
