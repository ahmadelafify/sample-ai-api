#!/usr/bin/env bash

set -o allexport
source .env
set +o allexport

gunicorn --bind=0.0.0.0:$API_PORT main:app
