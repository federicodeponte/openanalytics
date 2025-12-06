#!/bin/bash
# Start AEO Checks service with API keys from environment

set -e

echo "🚀 Starting AEO Checks Service with API Keys"
echo ""

# Check if API keys are set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  OPENROUTER_API_KEY not set"
    echo "   Set it with: export OPENROUTER_API_KEY=your_key"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   Set it with: export OPENAI_API_KEY=your_key"
fi

echo ""
echo "Starting service on port 8000..."
echo ""

cd "$(dirname "$0")"
source venv/bin/activate

# Kill existing service
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 1

# Start service with API keys
PYTHONPATH=..:.:$PYTHONPATH uvicorn main:app --host 0.0.0.0 --port 8000 --reload

