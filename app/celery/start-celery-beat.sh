#!/bin/bash

set -o errexit
set -o nounset

DATA_DIR=".celery"
PID_FILE="$DATA_DIR/celerybeat.pid"

mkdir -p "$DATA_DIR"
rm -f "$PID_FILE"

celery -A app.main.celery beat -l info
