#!/bin/bash

# Check if the migration name is provided as a parameter
if [ $# -eq 0 ]; then
    echo "Migration name missing. Usage: $0 <migration_name>"
    exit 1
fi

# Run the Alembic revision command with autogenerate
alembic revision --autogenerate -m "$1"
