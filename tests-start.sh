#! /usr/bin/env bash

CONFIG_FILE=${CONFIG_FILE:-".env.test"}

set -o allexport

source $CONFIG_FILE

alembic upgrade head

python ./tests_pre_start.py

bash ./scripts/test.sh "$@"
