#!/usr/bin/env python3
"""Enhanced configuration handler with store name mapping and SMS support."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from confighandler import ConfigHandler
from sms_notifier import StoreMapper, SMSNotifier


class EnhancedConfigHandler(ConfigHandler):
    """Enhanced configuration handler with store mapping and SMS support."""

    def __init__(
        self, path_to_config_file="./config.toml", sms_config_file="./sms_config.json"
    ):
        super().__init__(path_to_config_file)
        self.sms_config_file = sms_config_file
        self.store_mapper = StoreMapper()
        self.sms_notifier = None
        self.load_sms_config()

    def load_sms_config(self):
        """Load SMS configuration."""
        if os.path.exists(self.sms_config_file):
            try:
                with open(self.sms_config_file, "r") as f:
                    self.sms_config = json.load(f)
                self.sms_notifier = SMSNotifier(
                    self.sms_config.get("sms", {}).get("methods", {})
                )
            except Exception as e:
                print(f"❌ Error loading SMS config: {e}")
                self.sms_config = {}
                self.sms_notifier = None
        else:
            self.sms_config = {}
            self.sms_notifier = None

    def resolve_store_names_to_ids(self) -> List[str]:
        """Convert store names to store IDs."""
        store_names = self.searchconfig.selected_stores
        if not store_names:
            return []

        store_ids = []
        default_zip = self.sms_config.get("store_mapping", {}).get(
            "default_zip", "97223"
        )

        for store_name in store_names:
            # Check if it's already a store ID (starts with R)
            if store_name.startswith("R") and len(store_name) == 4:
                store_ids.append(store_name)
                print(f"✅ Using store ID: {store_name}")
            else:
                # Try to find store ID by name
                store_id = self.store_mapper.find_store_id(store_name, default_zip)
                if store_id:
                    store_ids.append(store_id)
                    print(f"✅ Mapped '{store_name}' to store ID: {store_id}")
                else:
                    print(f"❌ Could not find store ID for: {store_name}")

        return store_ids

    def get_enhanced_search_config(self):
        """Get search configuration with resolved store IDs."""
        # Create a copy of the search config
        enhanced_config = self.searchconfig

        # Resolve store names to IDs
        resolved_store_ids = self.resolve_store_names_to_ids()

        # Update the stores list
        enhanced_config.selected_stores = resolved_store_ids

        return enhanced_config

    def send_sms_notification(self, message: str) -> bool:
        """Send SMS notification if configured."""
        if not self.sms_notifier:
            return False

        return self.sms_notifier.send_notification(message)


class EnhancedCallbacks:
    """Enhanced callbacks with SMS support."""

    def __init__(self, config_handler: EnhancedConfigHandler):
        self.config_handler = config_handler
        self.sms_enabled = config_handler.sms_config.get("sms", {}).get(
            "enabled", False
        )

    async def on_stock_available(self, message):
        """Handle stock available notification."""
        print(f"✅ STOCK AVAILABLE: {message}")

        if self.sms_enabled:
            sms_message = f"🎉 iPhone 17 Pro is now available!\n\n{message}"
            self.config_handler.send_sms_notification(sms_message)

    async def on_newly_available(self):
        """Handle newly available notification."""
        print("🆕 NEWLY AVAILABLE!")

        if self.sms_enabled:
            sms_message = (
                "🚨 URGENT: iPhone 17 Pro just became available! Check Apple Store now!"
            )
            self.config_handler.send_sms_notification(sms_message)

    async def on_appointment_available(self, message):
        """Handle appointment available notification."""
        print(f"📅 APPOINTMENT AVAILABLE: {message}")

        if self.sms_enabled:
            sms_message = f"📅 Apple Store appointment available!\n\n{message}"
            self.config_handler.send_sms_notification(sms_message)

    async def on_start(self):
        """Handle monitoring start."""
        print("🚀 Starting monitoring...")

        if self.sms_enabled:
            sms_message = "🔍 Apple Store monitoring started for iPhone 17 Pro"
            self.config_handler.send_sms_notification(sms_message)

    async def on_stop(self):
        """Handle monitoring stop."""
        print("🛑 Stopping monitoring...")

    async def on_auto_report(self, message):
        """Handle auto report."""
        print(f"📊 AUTO REPORT: {message}")

    async def on_connection_error(self, message):
        """Handle connection error."""
        print(f"🔌 CONNECTION ERROR: {message}")

    async def on_error(self, error, logfile_path):
        """Handle error."""
        print(f"❌ ERROR: {error}")
        if logfile_path:
            print(f"📝 Log file: {logfile_path}")

    async def on_proxy_depletion(self, message):
        """Handle proxy depletion."""
        print(f"🔄 PROXY DEPLETION: {message}")

    async def on_long_processing_warning(self, message):
        """Handle long processing warning."""
        print(f"⏰ LONG PROCESSING: {message}")


def create_enhanced_config():
    """Create an enhanced configuration with store names."""
    config_content = """# Enhanced Apple Store Stock Notifier Configuration

[search]
device_family = "iphone17pro"     # the device family
models = ["MG7Q4LL/A"] # the device types
carriers = ["UNLOCKED/US"]          # the carriers, if applicable
country_code = "us"                 # the country code
zip_code = "97223"                  # the zip-code area, can be left empty to use specific stores
stores = ["Washington Square"] # store names (will be mapped to store IDs automatically)

[general]
polling_interval_seconds = 120 # recommended to make it > 10 seconds to account for processing time, make it > 30 when using random proxies
report_after_n_counts = 30     # after how many times a report should be generated
data_path = "data.csv"
log_path = "log.txt"
randomize_proxies = false

[sms]
enabled = true
phone_number = ""              # Your phone number (10 digits)
carrier = "verizon"            # Your carrier (verizon, att, tmobile, sprint, etc.)
email = ""                     # Your Gmail address
email_password = ""            # Your Gmail app password

[telegram]
username = ""                      # Your Telegram username (messages will be sent to this user)
api_id = ""                        # Telegram bot API ID (usually an 8-digit number)
api_hash = ""                      # Telegram bot API hash
bot_token = ""                     # Telegram bot token
session_name = "iPhone17ProFinder" # A unique name to create the virtual telegram client
"""

    with open("config_enhanced.toml", "w") as f:
        f.write(config_content)

    print("✅ Created config_enhanced.toml with store name support")
    print("📝 Please edit the file with your preferences")


if __name__ == "__main__":
    # Test the enhanced configuration
    print("🧪 Testing Enhanced Configuration System")
    print("=" * 50)

    # Create enhanced config
    create_enhanced_config()

    # Test store mapping
    mapper = StoreMapper()
    store_id = mapper.find_store_id("Apple Washington Square", "97223")
    if store_id:
        print(f"✅ Found Apple Washington Square: {store_id}")
    else:
        print("❌ Could not find Apple Washington Square")

    print("\n✅ Enhanced configuration system ready!")
    print("\n📋 Next steps:")
    print("1. Edit config_enhanced.toml with your preferences")
    print("2. Set up SMS notifications (optional)")
    print("3. Run the enhanced monitor")
