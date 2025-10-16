#!/usr/bin/env python3
"""
DIY SMS Gateway for Home Assistant on Raspberry Pi
Based on: https://tomerklein.dev/diy-sms-gateway-send-messages-anytime-anywhere-c70b20c91077
"""

import requests
import json
from typing import Dict, Optional
import logging


class HomeAssistantSMSGateway:
    """SMS Gateway using Home Assistant REST API on Raspberry Pi."""

    def __init__(
        self,
        ha_url: str,
        ha_token: str,
        entity_id: str = "notify.mobile_app_your_phone",
    ):
        """
        Initialize Home Assistant SMS Gateway.

        Args:
            ha_url: Home Assistant URL (e.g., "http://192.168.1.100:8123")
            ha_token: Long-lived access token from Home Assistant
            entity_id: Notification entity ID for your phone
        """
        self.ha_url = ha_url.rstrip("/")
        self.ha_token = ha_token
        self.entity_id = entity_id
        self.headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }

    def send_sms(self, message: str, title: str = "Stock Alert") -> bool:
        """Send SMS via Home Assistant notification service."""
        try:
            url = f"{self.ha_url}/api/services/notify/{self.entity_id.split('.')[1]}"

            data = {
                "message": message,
                "title": title,
                "data": {"push": {"sound": "default", "badge": 1}},
            }

            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()

            print(f"✅ SMS sent via Home Assistant: {title}")
            return True

        except Exception as e:
            print(f"❌ Failed to send SMS via Home Assistant: {e}")
            return False

    def test_connection(self) -> bool:
        """Test connection to Home Assistant."""
        try:
            url = f"{self.ha_url}/api/"
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()

            print("✅ Home Assistant connection successful")
            return True

        except Exception as e:
            print(f"❌ Home Assistant connection failed: {e}")
            return False


class RaspberryPiSMSGateway:
    """Direct SMS Gateway using GSM module on Raspberry Pi."""

    def __init__(self, serial_port: str = "/dev/ttyUSB0", baud_rate: int = 9600):
        """
        Initialize Raspberry Pi SMS Gateway with GSM module.

        Args:
            serial_port: Serial port for GSM module (usually /dev/ttyUSB0)
            baud_rate: Baud rate for serial communication
        """
        self.serial_port = serial_port
        self.baud_rate = baud_rate

    def send_sms_gsm(self, phone_number: str, message: str) -> bool:
        """Send SMS directly via GSM module."""
        try:
            import serial
            import time

            # Open serial connection
            ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            time.sleep(2)

            # AT commands to send SMS
            commands = [
                "AT\r\n",  # Test connection
                "AT+CMGF=1\r\n",  # Set SMS text mode
                f'AT+CMGS="{phone_number}"\r\n',  # Set recipient
                f"{message}\x1A",  # Message + Ctrl+Z
            ]

            for cmd in commands:
                ser.write(cmd.encode())
                time.sleep(1)
                response = ser.read(ser.in_waiting).decode()
                print(f"GSM Response: {response.strip()}")

            ser.close()
            print(f"✅ SMS sent directly via GSM to {phone_number}")
            return True

        except Exception as e:
            print(f"❌ Failed to send SMS via GSM: {e}")
            return False


class WebhookSMSGateway:
    """Simple webhook-based SMS gateway for Raspberry Pi."""

    def __init__(self, webhook_url: str, webhook_secret: str = None):
        """
        Initialize webhook SMS gateway.

        Args:
            webhook_url: Your Raspberry Pi webhook endpoint
            webhook_secret: Optional secret for authentication
        """
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret

    def send_sms_webhook(self, phone_number: str, message: str) -> bool:
        """Send SMS via custom webhook on Raspberry Pi."""
        try:
            data = {
                "phone": phone_number,
                "message": message,
                "timestamp": int(time.time()),
            }

            headers = {"Content-Type": "application/json"}
            if self.webhook_secret:
                headers["Authorization"] = f"Bearer {self.webhook_secret}"

            response = requests.post(
                self.webhook_url, json=data, headers=headers, timeout=10
            )
            response.raise_for_status()

            print(f"✅ SMS sent via webhook to {phone_number}")
            return True

        except Exception as e:
            print(f"❌ Failed to send SMS via webhook: {e}")
            return False


# Integration with existing SMS notifier
def create_ha_sms_config():
    """Create Home Assistant SMS configuration."""
    config = {
        "sms": {
            "enabled": True,
            "methods": {
                "home_assistant": {
                    "enabled": True,
                    "ha_url": "http://192.168.1.100:8123",
                    "ha_token": "your-long-lived-access-token",
                    "entity_id": "notify.mobile_app_your_phone",
                },
                "raspberry_pi_gsm": {
                    "enabled": False,
                    "serial_port": "/dev/ttyUSB0",
                    "baud_rate": 9600,
                    "phone_number": "1234567890",
                },
                "webhook": {
                    "enabled": False,
                    "webhook_url": "http://192.168.1.100:5000/send_sms",
                    "webhook_secret": "your-secret-key",
                    "phone_number": "1234567890",
                },
            },
        }
    }

    with open("ha_sms_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Created ha_sms_config.json")
    print("📝 Edit with your Home Assistant details")


if __name__ == "__main__":
    import time

    # Test Home Assistant SMS
    print("🏠 Testing Home Assistant SMS Gateway...")

    # Replace with your Home Assistant details
    ha_gateway = HomeAssistantSMSGateway(
        ha_url="http://192.168.1.100:8123",
        ha_token="your-token-here",
        entity_id="notify.mobile_app_your_phone",
    )

    if ha_gateway.test_connection():
        test_message = "🍎 Test: iPhone 17 Pro available at Apple Store!"
        ha_gateway.send_sms(test_message, "Stock Alert Test")

    # Create config template
    create_ha_sms_config()
