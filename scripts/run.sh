#!/usr/bin/env bash

set -o allexport
source .env
set +o allexport

source scripts/activate_venv.sh

uvicorn --host=0.0.0.0 --workers=$WORKER_COUNT --port=$API_PORT --ws=websockets main:app