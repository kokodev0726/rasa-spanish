# 1. Base image with Python 3.10.18
FROM python:3.10.18-slim

# 2. Install system dependencies for Rasa
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
      curl \
      libssl-dev \
      libffi-dev \
      libxml2-dev \
      libxslt1-dev && \
    rm -rf /var/lib/apt/lists/*

# 3. Create app directory
WORKDIR /app

# 4. Copy your project in
COPY . /app

# 5. Install Python dependencies, including Rasa & SDK
#    Pin to 3.6.2 to match your host setup
RUN pip install --upgrade pip setuptools wheel && \
    pip install \
      "rasa==3.6.21" \
      "rasa-sdk==3.6.2" \
      --no-cache-dir -r requirements.txt

# 6. (Optional) Train your model at build time
RUN rasa train

# 7. Expose the port
EXPOSE 5005

# 8. Launch Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
