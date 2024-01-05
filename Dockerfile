FROM python:3.10-slim

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./start_app.sh
ENTRYPOINT ["./start_app.sh"]
