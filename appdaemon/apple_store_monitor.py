import appdaemon.plugins.hass.hassapi as hass
import requests
import schedule
import time
import threading
from datetime import datetime


class AppleStoreMonitor(hass.Hass):

    def initialize(self):
        """Initialize the Apple Store Monitor"""
        self.log("Initializing Apple Store Monitor")

        # Get configuration
        self.sms_gateway_url = self.args.get(
            "sms_gateway_url", "http://192.168.1.100:5000"
        )
        self.check_interval = self.args.get("check_interval", 300)  # 5 minutes default
        self.stores = self.args.get("stores", [])
        self.products = self.args.get("products", [])

        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(
            target=self.start_monitoring, daemon=True
        )
        self.monitor_thread.start()

        self.log(
            f"Apple Store Monitor started with {len(self.stores)} stores and {len(self.products)} products"
        )

    def start_monitoring(self):
        """Start the monitoring loop"""
        schedule.every(self.check_interval).seconds.do(self.check_stock)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def check_stock(self):
        """Check stock for configured products and stores"""
        self.log("Checking Apple Store stock...")

        try:
            # Import your existing monitor logic here
            from run_monitor import StockMonitor

            monitor = StockMonitor()
            results = monitor.check_all_stores()

            # Process results and send notifications
            for result in results:
                if result.get("in_stock"):
                    self.send_notification(result)

        except Exception as e:
            self.log(f"Error checking stock: {e}", level="ERROR")

    def send_notification(self, stock_info):
        """Send SMS notification via gateway"""
        try:
            message = f"🍎 STOCK ALERT: {stock_info['product']} is available at {stock_info['store']}!"

            # Send via SMS gateway
            response = requests.post(
                f"{self.sms_gateway_url}/send_sms", json={"message": message}
            )

            if response.status_code == 200:
                self.log(f"SMS sent successfully: {message}")

                # Also create Home Assistant notification
                self.call_service(
                    "notify/mobile_app_your_phone",
                    title="Apple Stock Alert",
                    message=message,
                )
            else:
                self.log(f"Failed to send SMS: {response.text}", level="ERROR")

        except Exception as e:
            self.log(f"Error sending notification: {e}", level="ERROR")
