# Apple Store Stock Notifier

Monitor Apple Store stock availability and get SMS notifications when products become available.

## Features

- **Real-time Stock Monitoring**: Continuously monitors Apple Store stock for specified products
- **SMS Notifications**: Sends instant SMS alerts when products become available
- **Multiple Store Support**: Monitor stock across different Apple Store locations
- **Home Assistant Integration**: Native integration with sensors and notification services
- **Raspberry Pi SMS Gateway**: Includes companion SMS gateway for Raspberry Pi

## Requirements

- Home Assistant 2023.1.0 or newer
- SMS Gateway (Raspberry Pi with SMS modem or external SMS service)
- HACS (Home Assistant Community Store)

## Installation

1. Install via HACS:
   - Go to HACS → Integrations
   - Click the three dots menu → Custom repositories
   - Add this repository URL
   - Install "Apple Store Stock Notifier"

2. Restart Home Assistant

3. Add the integration:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "Apple Store Stock Notifier"
   - Follow the configuration steps

## Configuration

During setup, you'll need to provide:

- **SMS Gateway URL**: URL of your SMS gateway (e.g., `http://192.168.1.100:5000`)
- **Check Interval**: How often to check stock (5-60 minutes, default: 10 minutes)
- **Phone Numbers**: Comma-separated list of phone numbers for notifications

## Usage

Once configured, the integration provides:

### Sensors
- `sensor.apple_store_stock`: Shows current stock status and last check time

### Services
- `notify.apple_store_sms`: Send SMS notifications
- `apple_store_notifier.check_stock`: Manually trigger stock check

### Automation Example

```yaml
automation:
  - alias: "iPhone Available Alert"
    trigger:
      - platform: state
        entity_id: sensor.apple_store_stock
        attribute: products_in_stock
        to: "1"
    action:
      - service: notify.apple_store_sms
        data:
          message: "iPhone 15 Pro is now available at Apple Store!"
          target: "+1234567890"
```

## SMS Gateway Setup

For the complete SMS gateway setup on Raspberry Pi, see the included `RASPBERRY_PI_SMS_SETUP.md` guide.

## Support

For issues and feature requests, please use the GitHub repository issue tracker.