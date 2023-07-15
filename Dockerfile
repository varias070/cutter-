FROM python:3.8

WORKDIR /app

COPY req.text ./
RUN pip install -r req.text
COPY . .
RUN python3 server.py


CMD ["python3", "server.py"]