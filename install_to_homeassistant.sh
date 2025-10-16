#!/bin/bash

# Installation script for Apple Store Stock Notifier
# Run this script to install the integration to your Home Assistant

echo "🍎 Installing Apple Store Stock Notifier to Home Assistant..."

# Check if Home Assistant config path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/homeassistant/config"
    echo "Example: $0 /home/homeassistant/.homeassistant"
    echo "Or: $0 /config (if running in Home Assistant OS)"
    exit 1
fi

HA_CONFIG_PATH="$1"
CUSTOM_COMPONENTS_PATH="$HA_CONFIG_PATH/custom_components"

# Create custom_components directory if it doesn't exist
mkdir -p "$CUSTOM_COMPONENTS_PATH"

# Copy the integration
echo "📁 Copying integration files..."
cp -r custom_components/apple_store_notifier "$CUSTOM_COMPONENTS_PATH/"

echo "✅ Integration installed successfully!"
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services"
echo "3. Click 'Add Integration'"
echo "4. Search for 'Apple Store Stock Notifier'"
echo "5. Configure with your SMS gateway URL"
echo ""
echo "SMS Gateway URL example: http://192.168.1.100:5000"