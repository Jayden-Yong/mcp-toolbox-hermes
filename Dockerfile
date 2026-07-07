FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /tmp && chmod 1777 /tmp

COPY . .

EXPOSE 8931

CMD ["python", "server.py"]