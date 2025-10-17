#!/bin/bash

# SMS Service Installation Script for Home Assistant Pi

echo "📱 Installing SMS Service on Home Assistant Pi..."

# Create service directory
sudo mkdir -p /opt/sms_service
sudo cp sms_gateway.py /opt/sms_service/
sudo cp sms_config.json /opt/sms_service/
sudo cp requirements.txt /opt/sms_service/

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r /opt/sms_service/requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/sms-gateway.service > /dev/null <<EOF
[Unit]
Description=SMS Gateway Service
After=network.target

[Service]
Type=simple
User=homeassistant
WorkingDirectory=/opt/sms_service
ExecStart=/usr/bin/python3 /opt/sms_service/sms_gateway.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable sms-gateway.service

echo "✅ SMS Service installed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit /opt/sms_service/sms_config.json with your email settings"
echo "2. sudo systemctl start sms-gateway"
echo "3. Test: curl http://localhost:5000/health"
echo ""
echo "🔧 Configuration file: /opt/sms_service/sms_config.json"