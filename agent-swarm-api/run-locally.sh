#!/bin/sh

# set -a; source .env; set +a
export PYTHONPATH=$(pwd)/src && uvicorn app.main:app --port 8080 --reload