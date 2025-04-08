#!/bin/bash

BASE_URL="http://localhost:5050"

ENDPOINTS=(
  "/logs/info"
  "/logs/error"
  "/logs/warn"
  "/"
)

function random_index {
  echo $(( RANDOM % ${#ENDPOINTS[@]} ))
}

# Main loop
while true; do
  INDEX=$(random_index)
  ENDPOINT=${ENDPOINTS[$INDEX]}

  echo "Pinging $BASE_URL$ENDPOINT ..."
  curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL$ENDPOINT"

  sleep 5
done
