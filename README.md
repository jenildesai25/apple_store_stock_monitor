# Apple Store Stock Notifier for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that monitors Apple Store stock availability and sends SMS notifications when iPhones become available for pickup.

## Features

- 🍎 Monitor multiple Apple Stores for iPhone availability
- 📱 Track multiple iPhone models (iPhone 15 Pro series)
- 📲 SMS notifications via separate SMS gateway
- 🏠 Native Home Assistant integration with sensors
- ⚙️ Configurable check intervals
- 📊 Detailed availability tracking

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/jenildesai25/apple_store_stock_monitor` and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/apple_store_notifier` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Apple Store Stock Notifier"
4. Configure:
   - **SMS Gateway URL**: URL of your SMS gateway service (e.g., `http://192.168.1.100:5000`)
   - **Check Interval**: How often to check (5-60 minutes, default: 10 minutes)
   - **Stores**: Select Apple Stores to monitor
   - **Products**: Select iPhone models to track

## SMS Gateway Setup

This integration requires a separate SMS gateway service. Deploy the included SMS gateway on your Raspberry Pi:

```bash
# Copy the raspberry-pi-sms-gateway folder to your Pi
# Follow the setup instructions in RASPBERRY_PI_SMS_SETUP.md
```

## Entities Created

### Sensors
- `sensor.apple_store_stock_available` - Number of available items
- `sensor.apple_store_last_check` - Timestamp of last check

### Binary Sensors  
- `binary_sensor.apple_store_stock_available` - True when any stock is available

## Automation Example

```yaml
automation:
  - alias: "iPhone Stock Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.apple_store_stock_available
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🍎 iPhone Available!"
          message: "{{ state_attr('sensor.apple_store_stock_available', 'available_items') | length }} items available"
```

## Supported Stores

- Fifth Avenue (NYC)
- SoHo (NYC)  
- Upper West Side (NYC)
- Brooklyn (NYC)
- Staten Island (NYC)
- Queens Center (NYC)

## Supported Products

- iPhone 15 Pro (128GB, 256GB, 512GB, 1TB)
- iPhone 15 Pro Max (256GB, 512GB, 1TB)
- All in Natural Titanium

## Troubleshooting

Check the Home Assistant logs for any errors:
```
Settings → System → Logs
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License