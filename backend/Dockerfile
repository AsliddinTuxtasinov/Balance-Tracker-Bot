FROM python:3.12-alpine as builder


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apk update && apk add --no-cache \
    apk-tools \
    gettext \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    build-base \
    && pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
