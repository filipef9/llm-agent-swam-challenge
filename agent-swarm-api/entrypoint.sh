#!/bin/bash

export PYTHONUNBUFFERED=1
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

PYTHONPATH=/code uvicorn app.main:app --host 0.0.0.0 --port 8080