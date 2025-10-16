# Quick Setup Guide

## You Have 2 Options:

### Option A: Custom Integration (Recommended)
This runs inside Home Assistant and is easier to manage.

**Steps:**
1. **Install Integration:**
   ```bash
   # Copy integration to your Home Assistant
   ./install_to_homeassistant.sh /config
   ```

2. **Restart Home Assistant**

3. **Add Integration:**
   - Settings → Devices & Services
   - Add Integration → "Apple Store Stock Notifier"
   - Configure SMS gateway URL: `http://192.168.1.100:5000`

4. **Deploy SMS Gateway** (separate Pi):
   ```bash
   # On your SMS gateway Pi
   cd raspberry-pi-sms-gateway
   python src/sms_gateway/server.py
   ```

### Option B: Add-on (Alternative)
This runs as a Home Assistant add-on.

**Steps:**
1. **Copy add-on files** to `/addons/apple_store_notifier/`
2. **Install add-on** from Supervisor
3. **Configure and start**

## What Each Does:

- **Custom Integration**: Creates sensors in HA, sends SMS via gateway
- **Add-on**: Standalone service that monitors and sends SMS
- **SMS Gateway**: Separate service that actually sends SMS messages

## Recommended Setup:

```
[Home Assistant] → [Custom Integration] → [SMS Gateway Pi] → [SMS Modem]
```

The custom integration is cleaner and gives you more control within Home Assistant.