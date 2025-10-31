#!/bin/bash
cd /home/kavia/workspace/code-generation/to-do-notes-manager-216126-216135/backend_django_api
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

