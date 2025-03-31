#!/bin/bash

# Seed providers and patients
docker compose exec api python3 -m app.setup seed_users
