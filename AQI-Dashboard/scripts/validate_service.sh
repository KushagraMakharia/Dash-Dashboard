#!/bin/bash
# validate_service.sh

PORT=8050
RETRIES=5
DELAY=2

for i in $(seq 1 $RETRIES); do
  if nc -z localhost $PORT; then
    echo "Application is running on port $PORT"
    exit 0
  else
    echo "Attempt $i: Application is not running on port $PORT"
    sleep $DELAY
  fi
done

echo "Application failed to start after $RETRIES attempts."
exit 1
