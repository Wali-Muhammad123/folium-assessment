# Stage 1: Install dependencies and create a virtual environment
# Stage 1: Install dependencies and create a virtual environment
FROM python:3.9 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip && /venv/bin/pip install -r requirements.txt

# Copy the shell script to the container
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Stage 2: Copy the Django project and set the entry point
FROM base AS final

COPY ./warehouse/ /app/
EXPOSE 8000

# Set the entry point to run the shell script
ENTRYPOINT ["/app/entrypoint.sh"]



