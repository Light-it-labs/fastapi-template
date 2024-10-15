#!/bin/sh
set -e
set -x

# Detect if we're running in Git Bash on Windows
case "$(uname -s)" in
    MINGW*|CYGWIN*) 
        # We're in Git Bash on Windows
        export MSYS_NO_PATHCONV=1
        ;;
    *)
        # We're in a Unix-like environment
        ;;
esac

# Run formatting commands
ruff check --fix
ruff format
mypy .
