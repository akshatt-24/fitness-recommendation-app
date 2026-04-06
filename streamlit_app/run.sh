"#!/bin/bash

# Fitness Categorization App - Quick Start Script

echo \"🚀 Starting Fitness Categorization App...\"
echo \"\"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo \"❌ Python 3 is not installed. Please install Python 3.8 or higher.\"
    exit 1
fi

echo \"✓ Python found: $(python3 --version)\"

# Check if requirements are installed
echo \"\"
echo \"📦 Checking dependencies...\"

if ! python3 -c \"import streamlit\" 2>/dev/null; then
    echo \"⚠️  Dependencies not found. Installing...\"
    pip install -r requirements.txt
else
    echo \"✓ Dependencies already installed\"
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo \"\"
    echo \"📝 Creating .env file from template...\"
    cp .env.example .env
    echo \"✓ .env file created (using SQLite by default)\"
fi

# Run the app
echo \"\"
echo \"✨ Launching application...\"
echo \"\"
echo \"╔════════════════════════════════════════════════════╗\"
echo \"║                                                    ║\"
echo \"║  Fitness Categorization App                        ║\"
echo \"║  Diet & Workout Recommendation System              ║\"
echo \"║                                                    ║\"
echo \"║  Once started, open your browser and navigate to:  ║\"
echo \"║  👉 http://localhost:8501                          ║\"
echo \"║                                                    ║\"
echo \"║  Press Ctrl+C to stop the server                   ║\"
echo \"║                                                    ║\"
echo \"╚════════════════════════════════════════════════════╝\"
echo \"\"

streamlit run app.py
"