FROM alpine:3.11

WORKDIR /zigchadapp

COPY requirements.txt .
COPY zigchad.py .

RUN apk update && apk add --no-cache python3 && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

CMD ["python3", "zigchad.py"]
