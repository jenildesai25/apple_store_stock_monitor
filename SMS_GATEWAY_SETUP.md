# SMS Gateway Setup Guide

## 🚀 **Step 1: Deploy SMS Gateway**

### **On a separate Pi/device (not your Home Assistant Pi):**

```bash
# 1. Clone or copy your SMS gateway code
cd /home/pi
git clone https://github.com/jenildesai25/apple_store_stock_monitor.git
cd apple_store_stock_monitor/raspberry-pi-sms-gateway

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure SMS gateway
nano config.json
```

### **Step 2: Configure SMS Gateway**

Edit `raspberry-pi-sms-gateway/config.json`:

```json
{
  "sms": {
    "enabled": true,
    "port": "/dev/ttyUSB0",
    "baudrate": 115200,
    "phone_number": "+1234567890"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "logging": {
    "level": "INFO",
    "file": "sms_gateway.log"
  }
}
```

### **Step 3: Start SMS Gateway**

```bash
# Start the SMS gateway server
cd raspberry-pi-sms-gateway
python src/sms_gateway/server.py

# Should show:
# * Running on http://0.0.0.0:5000
# SMS Gateway ready!
```

### **Step 4: Test SMS Gateway**

```bash
# Test from another device
curl -X POST http://192.168.1.100:5000/send_sms \
  -H "Content-Type: application/json" \
  -d '{"message": "Test SMS from gateway"}'

# Should return: {"status": "success", "message": "SMS sent"}
```

## 🏠 **Step 5: Configure Home Assistant Integration**

### **Update Integration Configuration:**

1. **Settings** → **Devices & Services**
2. **Find "Apple Store Stock Notifier"**
3. **Click "Configure"**
4. **Set SMS Gateway URL**: `http://192.168.1.100:5000`
   (Replace with your SMS gateway Pi's IP)

### **Or reconfigure the integration:**

1. **Delete current integration**
2. **Add integration again**
3. **Enter SMS Gateway URL**: `http://192.168.1.100:5000`
4. **Configure stores and iPhone models**

## 📱 **Step 6: Test End-to-End**

Once configured:

1. **Integration runs check** (every 10 minutes)
2. **If stock found** → **Automatically sends SMS**
3. **Check logs** in Home Assistant for SMS status

## 🔍 **Troubleshooting:**

### **SMS Gateway Issues:**
```bash
# Check if gateway is running
curl http://192.168.1.100:5000/health

# Check gateway logs
tail -f raspberry-pi-sms-gateway/sms_gateway.log
```

### **Home Assistant Issues:**
```
Settings → System → Logs
Search: "apple_store_notifier"
Look for SMS-related errors
```

## 🎯 **Network Setup:**

```
[Home Assistant Pi] → [SMS Gateway Pi] → [SMS Modem] → [Phone Network]
   (Integration)         (Flask Server)     (Hardware)      (Your Phone)
   
192.168.1.50:8123 → 192.168.1.100:5000 → /dev/ttyUSB0 → +1234567890
```

## ⚙️ **Alternative: Use Email-to-SMS (No Hardware)**

If you don't have SMS modem hardware:

```yaml
# Add to Home Assistant configuration.yaml
notify:
  - name: sms_via_email
    platform: smtp
    server: smtp.gmail.com
    port: 587
    sender: your-email@gmail.com
    username: your-email@gmail.com
    password: your-gmail-app-password
    recipient: 1234567890@vtext.com  # Your carrier's SMS gateway
```

Then set SMS Gateway URL to: `http://localhost:8123` (dummy) and use HA automations for SMS.