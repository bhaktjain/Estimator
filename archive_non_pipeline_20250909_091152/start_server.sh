#!/bin/bash

# Set the OpenAI API key from environment variable
export OPENAI_API_KEY="${OPENAI_API_KEY}"

# Activate virtual environment
source venv/bin/activate

# Start the Flask server
echo "🚀 Starting Renovation Estimation API with API key set..."
echo "🔑 API Key: ${OPENAI_API_KEY:0:20}..."
python3 app.py 