#!/bin/bash
cd /tmp/kavia/workspace/code-generation/minimalist-todo-application-5012-5034/todo_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

