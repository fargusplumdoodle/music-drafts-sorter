#!/bin/sh
set -e

cd /code
.venv/bin/python main.py "$@"
