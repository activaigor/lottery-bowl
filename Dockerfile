FROM python:3.11-alpine AS base
ENV VIRTUAL_ENV=/app/.venv
RUN mkdir /app 
COPY pyproject.toml ./
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . /app
WORKDIR /app