#!/bin/bash
# start_server.sh

# Define the port number (in this case, 8050)
PORT=8050

# Check if the port is in use
if sudo lsof -i :$PORT; then
  echo "Port $PORT is already in use. Killing the process..."

  # Get the PID of the process using the port and kill it
  PID=$(sudo lsof -t -i :$PORT)
  sudo kill -9 $PID

  # Check if the process was killed
  if [ $? -eq 0 ]; then
    echo "Process on port $PORT has been killed."
  else
    echo "Failed to kill the process on port $PORT." >&2
    exit 1
  fi
else
  echo "Port $PORT is free."
fi

# Change to the app directory
cd /home/ec2-user/app

# Activate the virtual environment
if source venv/bin/activate; then
  echo "Virtual environment activated successfully."
else
  echo "Failed to activate virtual environment." >&2
  exit 1
fi

# Start the Dash app on port 8050 and run it in the background
echo "Starting Dash app on port $PORT..."
nohup python main.py > server.log 2>&1 &

# Check if the app started successfully
if [ $? -eq 0 ]; then
  echo "Dash app started successfully on port $PORT."
else
  echo "Failed to start Dash app." >&2
  exit 1
fi
