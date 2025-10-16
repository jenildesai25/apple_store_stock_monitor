#!/usr/bin/env python3
"""
Simple SMS webhook server for Raspberry Pi
Run this on your Raspberry Pi to receive SMS requests
"""

from flask import Flask, request, jsonify
import json
import logging
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
SMS_LOG_FILE = "sms_log.json"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")


def log_sms(phone_number: str, message: str, status: str):
    """Log SMS attempts to file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "phone": phone_number,
        "message": message,
        "status": status,
    }

    try:
        if os.path.exists(SMS_LOG_FILE):
            with open(SMS_LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]

        with open(SMS_LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        app.logger.error(f"Failed to log SMS: {e}")


def send_sms_via_gammu(phone_number: str, message: str) -> bool:
    """Send SMS using Gammu (requires GSM modem)."""
    try:
        import subprocess

        # Use gammu to send SMS
        cmd = ["gammu", "sendsms", "TEXT", phone_number, "-text", message]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            app.logger.info(f"SMS sent successfully to {phone_number}")
            return True
        else:
            app.logger.error(f"Gammu error: {result.stderr}")
            return False

    except Exception as e:
        app.logger.error(f"Failed to send SMS via Gammu: {e}")
        return False


def send_notification_via_ha(message: str, title: str = "Alert") -> bool:
    """Send notification via Home Assistant."""
    try:
        import requests

        ha_url = os.getenv("HA_URL", "http://localhost:8123")
        ha_token = os.getenv("HA_TOKEN")
        entity_id = os.getenv("HA_ENTITY_ID", "notify.mobile_app_phone")

        if not ha_token:
            app.logger.error("HA_TOKEN not set")
            return False

        url = f"{ha_url}/api/services/notify/{entity_id.split('.')[1]}"
        headers = {
            "Authorization": f"Bearer {ha_token}",
            "Content-Type": "application/json",
        }

        data = {"message": message, "title": title}

        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()

        app.logger.info("Notification sent via Home Assistant")
        return True

    except Exception as e:
        app.logger.error(f"Failed to send HA notification: {e}")
        return False


@app.route("/send_sms", methods=["POST"])
def send_sms():
    """Webhook endpoint to send SMS."""
    try:
        # Check authentication
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {WEBHOOK_SECRET}":
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        phone_number = data.get("phone")
        message = data.get("message")

        if not phone_number or not message:
            return jsonify({"error": "Phone number and message required"}), 400

        app.logger.info(f"SMS request: {phone_number[:3]}***{phone_number[-3:]}")

        # Try multiple methods
        success = False

        # Method 1: Try Gammu (GSM modem)
        if send_sms_via_gammu(phone_number, message):
            success = True
            log_sms(phone_number, message, "sent_gammu")

        # Method 2: Try Home Assistant notification
        elif send_notification_via_ha(message, "Stock Alert"):
            success = True
            log_sms(phone_number, message, "sent_ha")

        if success:
            return jsonify({"status": "sent", "timestamp": datetime.now().isoformat()})
        else:
            log_sms(phone_number, message, "failed")
            return jsonify({"error": "Failed to send SMS"}), 500

    except Exception as e:
        app.logger.error(f"SMS webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "methods": ["gammu", "home_assistant"],
        }
    )


@app.route("/logs", methods=["GET"])
def get_logs():
    """Get SMS logs."""
    try:
        if os.path.exists(SMS_LOG_FILE):
            with open(SMS_LOG_FILE, "r") as f:
                logs = json.load(f)
            return jsonify(logs[-10:])  # Last 10 entries
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🍓 Starting Raspberry Pi SMS Server...")
    print(f"📱 Webhook URL: http://YOUR_PI_IP:5000/send_sms")
    print(f"🔑 Secret: {WEBHOOK_SECRET}")
    print("📊 Status: http://YOUR_PI_IP:5000/status")

    app.run(host="0.0.0.0", port=5000, debug=False)
