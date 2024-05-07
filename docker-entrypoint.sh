#!/bin/bash

SERVER_PORT=${SERVER_PORT:-8000}

# Let the DB start
python api_pre_start.py

# Run migrations
alembic upgrade head

# Run application
if [ "$RUN_ENV" = "local" ]; then
  uvicorn app.main:app --host 0.0.0.0 --port ${SERVER_PORT} --reload
else
  LOG_JSON_FORMAT=true uvicorn app.main:app --host 0.0.0.0 --port ${SERVER_PORT} --proxy-headers
fi
