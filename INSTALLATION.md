# Installation Guide for Apple Store Stock Notifier

## Step 1: Install the Custom Integration

### Option A: Via HACS (Recommended)

1. **Add Custom Repository**:
   - Open HACS in Home Assistant
   - Go to "Integrations" 
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add your repository URL
   - Select "Integration" as category
   - Click "Add"

2. **Install Integration**:
   - Find "Apple Store Stock Notifier" in HACS
   - Click "Download"
   - Restart Home Assistant

### Option B: Manual Installation

1. **Copy Files**:
   ```bash
   # On your Home Assistant system
   cd /config
   mkdir -p custom_components
   # Copy the entire apple_store_notifier folder to custom_components/
   ```

2. **Restart Home Assistant**

## Step 2: Configure the Integration

1. **Add Integration**:
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "Apple Store Stock Notifier"
   - Click to add

2. **Configuration Options**:
   - **SMS Gateway URL**: `http://192.168.1.100:5000` (your SMS gateway)
   - **Check Interval**: 5 minutes (recommended)
   - **Stores**: Select NYC Apple Stores to monitor
   - **Products**: Select iPhone models you want

## Step 3: Set Up SMS Gateway (Separate)

The SMS gateway runs on a separate Raspberry Pi or device:

1. **Deploy SMS Gateway**:
   ```bash
   # On your SMS gateway device (separate Pi)
   git clone <your-repo>
   cd raspberry-pi-sms-gateway
   pip install -r requirements.txt
   python src/sms_gateway/server.py
   ```

2. **Configure SMS Gateway**:
   - Edit `config.json` with your SMS modem settings
   - Ensure it's accessible at the URL you configured

## Step 4: Create Automations

Add to your `automations.yaml`:

```yaml
- id: iphone_stock_alert
  alias: "iPhone Stock Available"
  trigger:
    - platform: state
      entity_id: binary_sensor.apple_store_stock_available
      to: "on"
  action:
    - service: notify.mobile_app_your_phone
      data:
        title: "🍎 iPhone Available!"
        message: >
          {% set items = state_attr('sensor.apple_store_stock_available', 'available_items') %}
          {% for item in items %}
          {{ item.product }} at {{ item.store }}
          {% endfor %}
        data:
          priority: high
          ttl: 0
```

## Step 5: Monitor and Test

1. **Check Entities**:
   - `sensor.apple_store_stock_available`
   - `binary_sensor.apple_store_stock_available`
   - `sensor.apple_store_last_check`

2. **View Logs**:
   ```
   Settings → System → Logs
   Filter by: apple_store_notifier
   ```

3. **Test SMS Gateway**:
   ```bash
   curl -X POST http://192.168.1.100:5000/send_sms \
     -H "Content-Type: application/json" \
     -d '{"message": "Test message"}'
   ```

## Troubleshooting

### Integration Not Loading
- Check Home Assistant logs
- Ensure all files are in correct location
- Restart Home Assistant

### SMS Not Sending  
- Verify SMS gateway is running
- Check SMS gateway logs
- Test gateway endpoint manually

### No Stock Updates
- Check internet connectivity
- Verify Apple Store codes are correct
- Check integration logs for errors

## Network Setup

```
[Home Assistant Pi] → [SMS Gateway Pi] → [SMS Modem] → [Phone Network]
     (Integration)        (Flask Server)     (Hardware)
```

The integration polls Apple's API and sends notifications via your SMS gateway when stock is found.