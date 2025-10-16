# 🍓 Raspberry Pi SMS Gateway Setup

## Overview
Create your own private SMS gateway using a Raspberry Pi and Home Assistant. No third-party services needed!

## Method 1: Home Assistant Notifications (Easiest)

### Setup Steps:
1. **Install Home Assistant** on your Raspberry Pi
2. **Install Home Assistant mobile app** on your phone
3. **Create Long-Lived Access Token**:
   - Go to Profile → Security → Long-Lived Access Tokens
   - Create token and copy it

### Configuration:
```json
{
  "home_assistant": {
    "enabled": true,
    "ha_url": "http://192.168.1.100:8123",
    "ha_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "entity_id": "notify.mobile_app_your_phone"
  }
}
```

## Method 2: GSM Modem (True SMS)

### Hardware Needed:
- Raspberry Pi 4
- USB GSM Modem (like SIM800L or Huawei E3372)
- SIM card with SMS plan

### Software Setup:
```bash
# Install Gammu
sudo apt update
sudo apt install gammu gammu-smsd

# Configure Gammu
sudo nano /etc/gammurc
```

Add to `/etc/gammurc`:
```
[gammu]
device = /dev/ttyUSB0
connection = at115200
```

### Test GSM Modem:
```bash
# Check if modem is detected
gammu identify

# Send test SMS
gammu sendsms TEXT 1234567890 -text "Test message"
```

## Method 3: Webhook Server

### Install on Raspberry Pi:
```bash
# Install dependencies
pip3 install flask requests

# Copy server file to Pi
scp raspberry_pi_sms_server.py pi@192.168.1.100:~/

# Run server
python3 raspberry_pi_sms_server.py
```

### Environment Variables:
```bash
export WEBHOOK_SECRET="your-secret-key"
export HA_URL="http://localhost:8123"
export HA_TOKEN="your-ha-token"
export HA_ENTITY_ID="notify.mobile_app_your_phone"
```

## Integration with Stock Checker

Update your `sms_notifier.py` to include Home Assistant method:

```python
def send_sms_home_assistant(self, message: str) -> bool:
    """Send SMS via Home Assistant."""
    try:
        config = self.config.get('home_assistant', {})
        if not config.get('enabled'):
            return False
        
        url = f"{config['ha_url']}/api/services/notify/{config['entity_id'].split('.')[1]}"
        headers = {
            "Authorization": f"Bearer {config['ha_token']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "message": message,
            "title": "Apple Stock Alert"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        print("✅ SMS sent via Home Assistant")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send HA SMS: {e}")
        return False
```

## Testing

### Test Home Assistant Connection:
```bash
python3 home_assistant_sms_server.py
```

### Test Webhook:
```bash
curl -X POST http://192.168.1.100:5000/send_sms \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"phone": "1234567890", "message": "Test from Pi!"}'
```

## Advantages

✅ **Complete Privacy** - No third-party services
✅ **No Rate Limits** - Send as many SMS as you want  
✅ **Free** - Only cost is SIM card plan
✅ **Reliable** - Local network, no internet dependencies
✅ **Customizable** - Full control over functionality

## Troubleshooting

### GSM Modem Issues:
```bash
# Check USB devices
lsusb

# Check serial ports
ls /dev/ttyUSB*

# Test AT commands
minicom -D /dev/ttyUSB0
```

### Home Assistant Issues:
- Check token permissions
- Verify mobile app is connected
- Test API endpoint manually

### Network Issues:
- Ensure Pi is accessible on local network
- Check firewall settings
- Verify port 5000 is open

---

**Your Raspberry Pi SMS gateway is now ready! 🎉**