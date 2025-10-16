#!/usr/bin/env python3
"""Simple runner script for the Apple Store Stock Notifier with enhanced features."""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_config import EnhancedConfigHandler, EnhancedCallbacks
from store_checker import StoreChecker


class SimpleMonitor:
    """Simple monitor with enhanced features."""

    def __init__(self, config_file="config_enhanced.toml"):
        self.config_file = config_file
        self.config_handler = EnhancedConfigHandler(config_file)
        self.callbacks = EnhancedCallbacks(self.config_handler)

        # Get enhanced search config with resolved store IDs
        self.search_config = self.config_handler.get_enhanced_search_config()

        # Initialize store checker
        self.store_checker = StoreChecker(
            self.callbacks,
            self.search_config,
            randomize_proxies=self.config_handler.get(["general", "randomize_proxies"]),
        )

    async def run_single_check(self):
        """Run a single stock check."""
        print("🔍 Running single stock check...")
        print(f"Device: {self.search_config.device_family}")
        print(f"Model: {self.search_config.selected_device_models}")
        print(f"Stores: {self.search_config.selected_stores}")
        print("-" * 50)

        try:
            availability, timestamp, processing_time = await self.store_checker.refresh(
                verbose=True
            )

            print(f"\n📊 Results:")
            print(
                f"Availability: {'✅ Available' if availability else '❌ Not Available'}"
            )
            print(f"Timestamp: {timestamp}")
            print(f"Processing time: {processing_time} seconds")

            return availability

        except Exception as e:
            print(f"❌ Error during check: {e}")
            return False

    async def run_monitoring(self):
        """Run continuous monitoring."""
        print("🔄 Starting continuous monitoring...")
        print("Press Ctrl+C to stop")
        print("-" * 50)

        polling_interval = self.config_handler.get(
            ["general", "polling_interval_seconds"]
        )
        count = 0

        try:
            while True:
                count += 1
                print(f"\n🔍 Check #{count}")

                availability = await self.run_single_check()

                if availability:
                    print("🎉 STOCK FOUND! Check the Apple Store website!")
                else:
                    print("😔 No stock available")

                print(f"⏰ Waiting {polling_interval} seconds until next check...")
                await asyncio.sleep(polling_interval)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")


def print_usage():
    """Print usage instructions."""
    print("🍎 Apple Store Stock Notifier")
    print("=" * 40)
    print("Usage:")
    print("  python run_monitor.py check    - Run single check")
    print("  python run_monitor.py monitor  - Run continuous monitoring")
    print("  python run_monitor.py setup    - Setup configuration")
    print("")
    print("Configuration files:")
    print("  config_enhanced.toml  - Main configuration")
    print("  sms_config.json       - SMS notification settings")
    print("")


def setup_configuration():
    """Setup configuration files."""
    print("🔧 Setting up configuration...")

    # Check if enhanced config exists
    if not os.path.exists("config_enhanced.toml"):
        print("Creating config_enhanced.toml...")
        from enhanced_config import create_enhanced_config

        create_enhanced_config()

    # Check if SMS config exists
    if not os.path.exists("sms_config.json"):
        print("Creating sms_config.json...")
        from sms_notifier import create_sms_config_template

        create_sms_config_template()

    print("\n✅ Configuration files created!")
    print("\n📝 Please edit the following files:")
    print("  - config_enhanced.toml (main settings)")
    print("  - sms_config.json (SMS notifications)")
    print("\n🔧 Configuration tips:")
    print("  - Use store names like 'Apple Washington Square' instead of store IDs")
    print("  - Set up SMS notifications for free using Gmail + carrier email gateways")
    print("  - Adjust polling_interval_seconds (120 = 2 minutes)")


async def main():
    """Main function."""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == "setup":
        setup_configuration()

    elif command == "check":
        try:
            monitor = SimpleMonitor()
            await monitor.run_single_check()
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try running 'python run_monitor.py setup' first")

    elif command == "monitor":
        try:
            monitor = SimpleMonitor()
            await monitor.run_monitoring()
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try running 'python run_monitor.py setup' first")

    else:
        print(f"❌ Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    asyncio.run(main())
