#!/bin/bash

BASE_URL="http://localhost:5050"

ENDPOINTS=(
  "/latency/fast"
  "/latency/slow"
  "/latency/medium"
  "/logs/info"
  "/logs/error"
  "/logs/warn"
  "/"
)


function random_index {
  echo $(( RANDOM % ${#ENDPOINTS[@]} ))
}

send_request() {
  local ENDPOINT=$1
  echo "Pinging $BASE_URL$ENDPOINT ..."
  curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL$ENDPOINT"
}


while true; do
  REQUEST_COUNT=$((10 + RANDOM % 100))
  
   echo "Sending $REQUEST_COUNT requests..."
  
  for ((i = 0; i < REQUEST_COUNT; i++)); do
    INDEX=$(random_index)
    ENDPOINT=${ENDPOINTS[$INDEX]}
    
    send_request "$ENDPOINT" &
  done

  wait
  
  SLEEP_FOR=$((0 + RANDOM % 2))
  sleep $SLEEP_FOR
done