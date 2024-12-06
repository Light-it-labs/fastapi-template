#!/bin/bash

set -o errexit
set -o nounset

celery -A app.main.celery worker -l info -c 1
