# Multi-stage Dockerfile for CERBERUS-FANGS LANCELOTT - Unified Security Toolkit

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app

# Install comprehensive system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nmap \
    wget \
    unzip \
    zip \
    golang-go \
    nodejs \
    npm \
    php \
    apache2-utils \
    hydra \
    sqlmap \
    masscan \
    nikto \
    dirb \
    gobuster \
    ffuf \
    wpscan \
    metasploit-framework \
    adb \
    fastboot \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Go tools
RUN go install github.com/tomnomnom/assetfinder@latest && \
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Copy unified requirements and install Python dependencies
COPY requirements-unified.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code and tools
COPY . .

# Build Go-based tools (Metabigor, Osmedeus)
RUN cd Metabigor && go mod tidy && go build -o metabigor main.go
RUN cd Osmedeus && go mod tidy && go build -o osmedeus main.go

# Setup Node.js dependencies for tools that need them
RUN if [ -d "SuperGateway" ]; then cd SuperGateway && npm install && npm run build; fi
RUN if [ -d "SuperCompat" ]; then cd SuperCompat && npm install; fi
RUN if [ -d "SuperCompat/packages/supercompat" ]; then cd SuperCompat/packages/supercompat && npm install && npm run build; fi
RUN if [ -d "Social-Analyzer" ]; then cd Social-Analyzer && npm install; fi

# Setup permissions for all tools
RUN chmod +x Argus/argus.py \
    Kraken/kraken.py \
    PhoneSploit-Pro/phonesploitpro.py \
    Social-Analyzer/app.py \
    Spiderfoot/sfwebui.py \
    Storm-Breaker/st.py \
    Webstor/webstor.py \
    THC-Hydra/hydra \
    dismap/dismap-enhanced

# Create necessary directories for all tools
RUN mkdir -p logs reports uploads static temp \
    Argus/reports \
    Kraken/logs \
    PhoneSploit-Pro/logs \
    RedTeam-ToolKit/media \
    Social-Analyzer/logs \
    Spiderfoot/logs \
    Storm-Breaker/logs \
    Webstor/logs \
    THC-Hydra/logs \
    dismap/output \
    Metabigor/output \
    Osmedeus/workspaces \
    && chown -R appuser:appuser /app

# Setup database for Django-based tools
RUN cd RedTeam-ToolKit && python manage.py migrate || true

# Copy tool configurations if they exist
RUN mkdir -p configs/

# Switch to non-root user
USER appuser

# Expose main port and tool-specific ports
EXPOSE 7777 8080 8081 8082 8083 8084 8085 8086 8087 8088 8089

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7777/api/v1/health || exit 1

# Run the unified FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7777"]
