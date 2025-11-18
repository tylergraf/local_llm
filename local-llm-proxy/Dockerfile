FROM python:3.11-alpine

# Install dependencies
RUN apk add --no-cache bash curl jq

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proxy server
COPY proxy_server.py .
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8080

CMD ["/run.sh"]
