#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A app.main.celery beat -l info
