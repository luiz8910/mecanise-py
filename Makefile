SHELL := /bin/bash

.PHONY: venv install run clean

PYTHON  ?= python3
VENV    := .venv
PIP     := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

venv:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip

install: venv
	$(PIP) install -r requirements.txt

# Executa a API FastAPI em modo dev
# (aponta para app.interfaces.http.fastapi_app:app)
run:
	APP_PORT=$${APP_PORT:-8000} \
	$(UVICORN) app.interfaces.http.fastapi_app:app --reload --port $${APP_PORT}

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ **/__pycache__
