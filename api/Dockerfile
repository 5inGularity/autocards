# Use the official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the necessary files to the container
COPY * /app/

# Install Poetry and the dependencies specified in pyproject.toml
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Set the environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set the command to run the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
