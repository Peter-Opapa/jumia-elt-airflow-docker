# Multi-stage Dockerfile for Jumia ELT Pipeline
FROM apache/airflow:2.7.1-python3.8 as base

# Set working directory
WORKDIR /opt/airflow

# Switch to root to install system dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements file
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /opt/airflow/src/
COPY airflow/dags/ /opt/airflow/dags/
COPY airflow/plugins/ /opt/airflow/plugins/

# Set environment variables
ENV PYTHONPATH="/opt/airflow/src:$PYTHONPATH"
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD airflow jobs check --job-type SchedulerJob --hostname "$${HOSTNAME}"

# Default command
CMD ["airflow", "webserver"]
