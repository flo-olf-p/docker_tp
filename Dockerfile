FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --n-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY stock.py .

CMD ["python3", "stock.py"]