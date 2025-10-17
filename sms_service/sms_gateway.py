#!/usr/bin/env python3
"""
Simple SMS Gateway using Email-to-SMS
Runs on same Pi as Home Assistant
"""

import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from datetime import datetime
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Load configuration
def load_config():
    config_file = os.path.join(os.path.dirname(__file__), "sms_config.json")
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
        return None


config = load_config()

# Carrier SMS gateways
CARRIER_GATEWAYS = {
    "verizon": "@vtext.com",
    "att": "@txt.att.net",
    "tmobile": "@tmomail.net",
    "sprint": "@messaging.sprintpcs.com",
    "boost": "@sms.myboostmobile.com",
    "cricket": "@sms.cricketwireless.net",
    "uscellular": "@email.uscc.net",
    "metropcs": "@mymetropcs.com",
}


def send_email_sms(phone_number, message, carrier="verizon"):
    """Send SMS via email-to-SMS gateway"""

    if not config:
        logger.error("No configuration loaded")
        return False

    try:
        # Clean phone number (remove +1, spaces, dashes)
        clean_phone = "".join(filter(str.isdigit, phone_number))
        if clean_phone.startswith("1") and len(clean_phone) == 11:
            clean_phone = clean_phone[1:]  # Remove country code

        # Get carrier gateway
        gateway = CARRIER_GATEWAYS.get(carrier.lower(), "@vtext.com")
        sms_email = f"{clean_phone}{gateway}"

        # Create email
        msg = MIMEMultipart()
        msg["From"] = config["email"]["sender"]
        msg["To"] = sms_email
        msg["Subject"] = ""  # Empty subject for SMS

        # Add message (keep it short for SMS)
        msg.attach(MIMEText(message[:160], "plain"))  # SMS limit 160 chars

        # Send email
        server = smtplib.SMTP(
            config["email"]["smtp_server"], config["email"]["smtp_port"]
        )
        server.starttls()
        server.login(config["email"]["username"], config["email"]["password"])

        text = msg.as_string()
        server.sendmail(config["email"]["sender"], sms_email, text)
        server.quit()

        logger.info(f"SMS sent to {phone_number} via {sms_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return False


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "SMS Gateway",
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/send_sms", methods=["POST"])
def send_sms():
    """Send SMS endpoint"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        message = data.get("message", "")
        phone_number = data.get("phone_number", config.get("default_phone", ""))
        carrier = data.get("carrier", config.get("default_carrier", "verizon"))

        if not message:
            return jsonify({"error": "No message provided"}), 400

        if not phone_number:
            return jsonify({"error": "No phone number provided"}), 400

        # Send SMS
        success = send_email_sms(phone_number, message, carrier)

        if success:
            return jsonify(
                {
                    "status": "success",
                    "message": "SMS sent successfully",
                    "timestamp": datetime.now().isoformat(),
                }
            )
        else:
            return jsonify({"status": "error", "message": "Failed to send SMS"}), 500

    except Exception as e:
        logger.error(f"Error in send_sms endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/test", methods=["GET"])
def test_sms():
    """Test SMS endpoint"""
    test_message = f"SMS Gateway test - {datetime.now().strftime('%H:%M:%S')}"

    success = send_email_sms(
        config.get("default_phone", ""),
        test_message,
        config.get("default_carrier", "verizon"),
    )

    if success:
        return jsonify({"status": "Test SMS sent successfully"})
    else:
        return jsonify({"status": "Test SMS failed"}), 500


if __name__ == "__main__":
    if not config:
        print("❌ Configuration not loaded. Please create sms_config.json")
        exit(1)

    print("🚀 Starting SMS Gateway...")
    print(f"📱 Default phone: {config.get('default_phone', 'Not set')}")
    print(f"📧 Email: {config.get('email', {}).get('sender', 'Not set')}")
    print("🌐 Server starting on http://localhost:5000")

    app.run(host="0.0.0.0", port=5000, debug=False)
