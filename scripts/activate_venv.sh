#!/usr/bin/env bash

env_name=venv
ACTIVATE_SCRIPT=$env_name/bin/activate # Linux
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
  echo "Cannot find venv activate script at $ACTIVATE_SCRIPT"
  ACTIVATE_SCRIPT=$env_name/Scripts/activate # Windows
  echo "Set venv activate script path to $ACTIVATE_SCRIPT"
fi
source $ACTIVATE_SCRIPT
