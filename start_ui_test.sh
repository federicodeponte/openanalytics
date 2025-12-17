#!/bin/bash

# AEO Mentions UI Testing Setup with Full Live Logging
echo "🚀 Starting AEO Services UI Test Environment"
echo "============================================"

# Kill any existing services
echo "🧹 Cleaning up existing services..."
pkill -f "uvicorn.*mentions_service"
pkill -f "uvicorn.*main:app"
sleep 2

# Set environment for detailed logging
export PYTHONUNBUFFERED=1
export LOG_LEVEL=INFO

# Start the main service with mentions endpoint
echo "🔧 Starting AEO Services with full logging..."
cd aeo-checks

# Start with detailed logging
python3 -m uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level info \
  --access-log &

SERVICE_PID=$!

echo "⏳ Waiting for service startup..."
sleep 5

# Check if service started successfully
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Service started successfully on http://localhost:8000"
    echo ""
    echo "📋 Available for UI Testing:"
    echo "   🌐 API Root: http://localhost:8000/"
    echo "   🔍 Mentions Check: http://localhost:8000/mentions/check"
    echo "   📊 Service Status: http://localhost:8000/status"
    echo ""
    echo "🎯 MENTIONS CHECK UI TEST:"
    echo "Use this curl command or Postman/Insomnia:"
    echo ""
    echo "curl -X POST 'http://localhost:8000/mentions/check' \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{"
    echo "    \"companyName\": \"SCAILE\","
    echo "    \"companyAnalysis\": {"
    echo "      \"companyInfo\": {"
    echo "        \"products\": [\"AI content generation platform\"],"
    echo "        \"services\": [\"Content creation services\"],"
    echo "        \"industry\": \"AI/Marketing Technology\","
    echo "        \"pain_points\": [\"content creation efficiency\"],"
    echo "        \"geographic_modifiers\": [\"German\"],"
    echo "        \"use_cases\": [\"automated blog generation\"]"
    echo "      },"
    echo "      \"competitors\": [{\"name\": \"Jasper\"}]"
    echo "    },"
    echo "    \"mode\": \"fast\","
    echo "    \"numQueries\": 10"
    echo "  }'"
    echo ""
    echo "📝 LIVE LOGS will appear below:"
    echo "===================================="
    
    # Show live logs
    wait $SERVICE_PID
else
    echo "❌ Failed to start service"
    exit 1
fi
