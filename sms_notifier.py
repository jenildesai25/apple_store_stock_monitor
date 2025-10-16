#!/usr/bin/env python3
"""Free SMS notification system using email-to-SMS gateways."""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import json
import os


class SMSNotifier:
    """Free SMS notification system using various free services."""

    def __init__(self, config: Dict):
        self.config = config
        self.carrier_gateways = {
            "verizon": "@vtext.com",
            "att": "@txt.att.net",
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
            "boost": "@smsmyboost.com",
            "cricket": "@sms.cricketwireless.net",
            "metropcs": "@mymetropcs.com",
            "uscellular": "@email.uscc.net",
            "virgin": "@vmobl.com",
        }

    def get_sms_email(self, phone_number: str, carrier: str) -> str:
        """Convert phone number to email address for SMS."""
        # Remove all non-digits
        clean_number = "".join(filter(str.isdigit, phone_number))

        # Ensure it's 10 digits
        if len(clean_number) == 11 and clean_number.startswith("1"):
            clean_number = clean_number[1:]
        elif len(clean_number) != 10:
            raise ValueError(f"Invalid phone number: {phone_number}")

        if carrier.lower() not in self.carrier_gateways:
            raise ValueError(f"Unsupported carrier: {carrier}")

        return f"{clean_number}{self.carrier_gateways[carrier.lower()]}"

    def send_sms_email(self, phone_number: str, carrier: str, message: str) -> bool:
        """Send SMS via email gateway."""
        try:
            sms_email = self.get_sms_email(phone_number, carrier)

            # Use Gmail SMTP (free)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.config["email"]
            msg["To"] = sms_email
            msg["Subject"] = "Apple Store Stock Alert"

            msg.attach(MIMEText(message, "plain"))

            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(self.config["email"], self.config["email_password"])
            text = msg.as_string()
            server.sendmail(self.config["email"], sms_email, text)
            server.quit()

            print(f"✅ SMS sent to {phone_number} via {carrier}")
            return True

        except Exception as e:
            print(f"❌ Failed to send SMS to {phone_number}: {e}")
            return False

    def send_sms_pushbullet(self, message: str) -> bool:
        """Send SMS via Pushbullet (free tier)."""
        try:
            if "pushbullet_token" not in self.config:
                return False

            url = "https://api.pushbullet.com/v2/pushes"
            headers = {
                "Access-Token": self.config["pushbullet_token"],
                "Content-Type": "application/json",
            }

            data = {"type": "note", "title": "Apple Store Stock Alert", "body": message}

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            print("✅ Push notification sent via Pushbullet")
            return True

        except Exception as e:
            print(f"❌ Failed to send Pushbullet notification: {e}")
            return False

    def send_sms_ifttt(self, message: str) -> bool:
        """Send SMS via IFTTT webhook (free)."""
        try:
            if "ifttt_key" not in self.config or "ifttt_event" not in self.config:
                return False

            url = f"https://maker.ifttt.com/trigger/{self.config['ifttt_event']}/with/key/{self.config['ifttt_key']}"

            data = {
                "value1": "Apple Store Stock Alert",
                "value2": message,
                "value3": "iPhone 17 Pro",
            }

            response = requests.post(url, json=data)
            response.raise_for_status()

            print("✅ Notification sent via IFTTT")
            return True

        except Exception as e:
            print(f"❌ Failed to send IFTTT notification: {e}")
            return False

    def send_notification(self, message: str) -> bool:
        """Send notification using all available methods."""
        success = False

        # Try email-to-SMS if configured
        if "phone_number" in self.config and "carrier" in self.config:
            if self.send_sms_email(
                self.config["phone_number"], self.config["carrier"], message
            ):
                success = True

        # Try Pushbullet
        if self.send_sms_pushbullet(message):
            success = True

        # Try IFTTT
        if self.send_sms_ifttt(message):
            success = True

        return success


class StoreMapper:
    """Map store names to store IDs using Apple's API."""

    def __init__(self):
        self.store_cache = {}
        self.base_url = "https://www.apple.com/shop/retail/pickup-message"

    def find_store_id(self, store_name: str, zip_code: str = None) -> Optional[str]:
        """Find store ID by store name."""
        # Check cache first
        cache_key = f"{store_name}_{zip_code or 'any'}"
        if cache_key in self.store_cache:
            return self.store_cache[cache_key]

        try:
            # Try with zip code first
            if zip_code:
                url = f"{self.base_url}?pl=true&parts.0=MG7Q4LL/A&location={zip_code}"
                store_id = self._search_stores(url, store_name)
                if store_id:
                    self.store_cache[cache_key] = store_id
                    return store_id

            # Try with common zip codes if no specific zip provided
            common_zips = ["97223", "97201", "97202", "97203", "97204", "97205"]
            for zip_code in common_zips:
                url = f"{self.base_url}?pl=true&parts.0=MG7Q4LL/A&location={zip_code}"
                store_id = self._search_stores(url, store_name)
                if store_id:
                    self.store_cache[cache_key] = store_id
                    return store_id

            print(f"❌ Store '{store_name}' not found")
            return None

        except Exception as e:
            print(f"❌ Error finding store '{store_name}': {e}")
            return None

    def _search_stores(self, url: str, store_name: str) -> Optional[str]:
        """Search stores in API response."""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                return None

            data = response.json()
            if "body" not in data or "stores" not in data["body"]:
                return None

            stores = data["body"]["stores"]

            # Look for exact match first
            for store in stores:
                if store.get("storeName", "").lower() == store_name.lower():
                    return store.get("storeNumber")

            # Look for partial match
            for store in stores:
                if store_name.lower() in store.get("storeName", "").lower():
                    return store.get("storeNumber")

            return None

        except Exception as e:
            print(f"❌ Error searching stores: {e}")
            return None

    def get_store_info(self, store_id: str) -> Optional[Dict]:
        """Get detailed store information by ID."""
        try:
            url = f"{self.base_url}?pl=true&parts.0=MG7Q4LL/A&store={store_id}"
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                return None

            data = response.json()
            if "body" not in data or "stores" not in data["body"]:
                return None

            stores = data["body"]["stores"]
            for store in stores:
                if store.get("storeNumber") == store_id:
                    return {
                        "store_id": store.get("storeNumber"),
                        "store_name": store.get("storeName"),
                        "city": store.get("city"),
                        "state": store.get("state"),
                        "address": store.get("address", {}),
                        "phone": store.get("phoneNumber"),
                    }

            return None

        except Exception as e:
            print(f"❌ Error getting store info: {e}")
            return None


def create_sms_config_template():
    """Create a template SMS configuration file."""
    config = {
        "sms": {
            "enabled": True,
            "methods": {
                "email_sms": {
                    "enabled": True,
                    "email": "your-email@gmail.com",
                    "email_password": "your-app-password",
                    "phone_number": "1234567890",
                    "carrier": "verizon",
                },
                "pushbullet": {"enabled": False, "token": "your-pushbullet-token"},
                "ifttt": {
                    "enabled": False,
                    "key": "your-ifttt-key",
                    "event": "apple_stock_alert",
                },
            },
        },
        "store_mapping": {"enabled": True, "default_zip": "97223"},
    }

    with open("sms_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Created sms_config.json template")
    print("📝 Please edit the file with your notification preferences")


if __name__ == "__main__":
    # Test the store mapper
    mapper = StoreMapper()

    # Test finding Apple Washington Square
    store_id = mapper.find_store_id("Apple Washington Square", "97223")
    if store_id:
        print(f"✅ Found store ID: {store_id}")
        store_info = mapper.get_store_info(store_id)
        if store_info:
            print(f"Store info: {store_info}")
    else:
        print("❌ Store not found")

    # Create config template
    create_sms_config_template()
