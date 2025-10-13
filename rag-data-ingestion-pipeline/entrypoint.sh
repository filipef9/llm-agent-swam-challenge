#!/bin/bash

export PYTHONUNBUFFERED=1
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

PYTHONPATH=/code python -m pipeline