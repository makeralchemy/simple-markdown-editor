#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing/Verifying dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting Markdown Editor..."
python3 main.py

echo "Application closed."
