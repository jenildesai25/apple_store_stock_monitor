#!/bin/bash

# Monitor Apple Store integration from command line

echo "🍎 Apple Store Stock Monitor Status"
echo "=================================="

# Check if Home Assistant is running
if pgrep -f "homeassistant" > /dev/null; then
    echo "✅ Home Assistant is running"
else
    echo "❌ Home Assistant is not running"
    exit 1
fi

# Check integration logs (requires access to HA logs)
echo ""
echo "📋 Recent Integration Activity:"
tail -n 20 /config/home-assistant.log | grep "apple_store_notifier" | tail -5

# Check entity states via HA REST API (if enabled)
echo ""
echo "📊 Current Stock Status:"
curl -s -H "Authorization: Bearer YOUR_LONG_LIVED_TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8123/api/states/sensor.apple_store_stock_available | \
     jq '.state, .attributes.last_check'

echo ""
echo "🔄 To manually trigger a check:"
echo "curl -X POST -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     http://localhost:8123/api/services/homeassistant/update_entity \\"
echo "     -d '{\"entity_id\": \"sensor.apple_store_stock_available\"}'"