#!/bin/bash

echo "🚨 SignalSAR - Starting Demo Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Initialize database
echo "🗄️  Initializing database with mock data..."
python3 init_db.py
echo "✓ Database ready"
echo ""

echo "=================================="
echo "🎉 Setup complete!"
echo ""
echo "To start the demo:"
echo "  python3 app.py"
echo ""
echo "Then open: http://localhost:5000"
echo "=================================="
