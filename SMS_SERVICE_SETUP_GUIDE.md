# SMS Service Setup Guide - Same Pi as Home Assistant

## 🚀 **Step 1: Install SMS Service**

### **Copy files to your Home Assistant Pi:**

```bash
# SSH into your Home Assistant Pi
ssh homeassistant@your-pi-ip

# Create directory and copy files
mkdir -p ~/sms_service
# Copy the sms_service folder contents to ~/sms_service/
```

### **Run installation:**

```bash
cd ~/sms_service
chmod +x install_sms_service.sh
./install_sms_service.sh
```

## 📧 **Step 2: Configure Email Settings**

### **Get Gmail App Password:**

1. **Go to Google Account** → **Security**
2. **Enable 2-Factor Authentication** (required)
3. **App Passwords** → **Generate password** for "SMS Gateway"
4. **Copy the 16-character password**

### **Edit configuration:**

```bash
sudo nano /opt/sms_service/sms_config.json
```

**Update with your details:**

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender": "your-actual-email@gmail.com",
    "username": "your-actual-email@gmail.com", 
    "password": "your-16-char-app-password"
  },
  "default_phone": "1234567890",
  "default_carrier": "verizon",
  "service": {
    "host": "0.0.0.0",
    "port": 5000
  }
}
```

### **Carrier Options:**
- **Verizon**: `verizon`
- **AT&T**: `att`
- **T-Mobile**: `tmobile`
- **Sprint**: `sprint`

## 🚀 **Step 3: Start SMS Service**

```bash
# Start the service
sudo systemctl start sms-gateway

# Check status
sudo systemctl status sms-gateway

# Enable auto-start
sudo systemctl enable sms-gateway
```

## 🧪 **Step 4: Test SMS Service**

### **Health Check:**
```bash
curl http://localhost:5000/health
```

### **Test SMS:**
```bash
curl -X POST http://localhost:5000/send_sms \
  -H "Content-Type: application/json" \
  -d '{"message": "Test SMS from Home Assistant Pi!"}'
```

### **Quick Test:**
```bash
curl http://localhost:5000/test
```

## 🏠 **Step 5: Configure Home Assistant Integration**

### **Update Integration:**

1. **Settings** → **Devices & Services**
2. **Find "Apple Store Stock Notifier"**
3. **Click "Configure"**
4. **Set SMS Gateway URL**: `http://localhost:5000`

## 📱 **Step 6: Test End-to-End**

Once configured:

1. **Integration checks stock** (every 10 minutes)
2. **If stock found** → **Sends SMS via email gateway**
3. **You receive SMS** on your phone

## 🔍 **Troubleshooting**

### **Service Issues:**
```bash
# Check service logs
sudo journalctl -u sms-gateway -f

# Restart service
sudo systemctl restart sms-gateway

# Check if port is open
netstat -tlnp | grep 5000
```

### **Email Issues:**
- **Gmail App Password**: Make sure 2FA is enabled
- **Carrier Gateway**: Verify your carrier's SMS gateway
- **Phone Number**: Use 10 digits, no +1

### **Integration Issues:**
```
Home Assistant → Settings → System → Logs
Search: "apple_store_notifier"
```

## 🎯 **Network Flow:**

```
[Apple Store API] → [HA Integration] → [SMS Service] → [Gmail SMTP] → [Carrier] → [Your Phone]
                     (localhost:8123)   (localhost:5000)   (smtp.gmail.com)
```

## ⚙️ **Service Management:**

```bash
# Start service
sudo systemctl start sms-gateway

# Stop service  
sudo systemctl stop sms-gateway

# Restart service
sudo systemctl restart sms-gateway

# Check status
sudo systemctl status sms-gateway

# View logs
sudo journalctl -u sms-gateway -f
```

## 📋 **Configuration Files:**

- **Service**: `/opt/sms_service/sms_gateway.py`
- **Config**: `/opt/sms_service/sms_config.json`
- **Systemd**: `/etc/systemd/system/sms-gateway.service`
- **Logs**: `sudo journalctl -u sms-gateway`