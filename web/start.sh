#!/bin/bash

echo "Starting DocMemory Web Interface..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if docmemory is installed
if ! python3 -c "import docmemory" &> /dev/null; then
    echo "DocMemory is not installed"
    echo "Installing DocMemory..."
    pip3 install docmemory || {
        echo "Failed to install DocMemory"
        exit 1
    }
fi

# Check if flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Flask is not installed"
    echo "Installing Flask..."
    pip3 install flask || {
        echo "Failed to install Flask"
        exit 1
    }
fi

# Start the server
echo "Starting DocMemory Web Interface on http://localhost:8000"
python3 server.py