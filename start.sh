#!/bin/bash
# Start script for Financial Assistant

echo "Starting Financial Assistant..."
echo "================================"

# Activate virtual environment
source venv/bin/activate

# Check if database exists
if [ ! -f "data/financial_assistant.db" ]; then
    echo "Database not found. Initializing..."
    python src/init_db.py
fi

# Start Flask application
echo ""
echo "Starting Flask server..."
echo "Access the application at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo "================================"
echo ""

python src/app.py

