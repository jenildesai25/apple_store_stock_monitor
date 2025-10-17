# SMS Integration Options

## 🎯 **Option 1: Home Assistant Automation (Recommended)**

### **Setup Steps:**

1. **Install Home Assistant Mobile App** on your phone
2. **Add this automation** to `automations.yaml`:

```yaml
- id: iphone_stock_notification
  alias: "iPhone Stock Available Notification"
  trigger:
    - platform: state
      entity_id: binary_sensor.apple_store_stock_available
      to: "on"
  action:
    # Mobile app notification
    - service: notify.mobile_app_YOUR_PHONE_NAME
      data:
        title: "🍎 iPhone Available!"
        message: >
          {% set items = state_attr('sensor.apple_store_stock_available', 'available_items') %}
          {% if items %}
            {% for item in items %}
            {{ item.product }} at {{ item.store }}
            {% endfor %}
          {% else %}
            iPhone stock found! Check the app for details.
          {% endif %}
        data:
          priority: high
          ttl: 0
          actions:
            - action: "open_apple_store"
              title: "Open Apple Store"
```

## 📧 **Option 2: Email-to-SMS (Free)**

### **Carrier SMS Gateways:**
- **Verizon**: `1234567890@vtext.com`
- **AT&T**: `1234567890@txt.att.net`
- **T-Mobile**: `1234567890@tmomail.net`
- **Sprint**: `1234567890@messaging.sprintpcs.com`

### **Configuration:**

1. **Add to `configuration.yaml`:**
```yaml
notify:
  - name: sms_notification
    platform: smtp
    server: smtp.gmail.com
    port: 587
    timeout: 15
    sender: your-email@gmail.com
    encryption: starttls
    username: your-email@gmail.com
    password: your-gmail-app-password
    recipient: YOUR_PHONE@vtext.com
```

2. **Add automation:**
```yaml
- id: iphone_sms_alert
  alias: "iPhone SMS Alert"
  trigger:
    - platform: state
      entity_id: binary_sensor.apple_store_stock_available
      to: "on"
  action:
    - service: notify.sms_notification
      data:
        message: "🍎 iPhone available! {{ states('sensor.apple_store_stock_available') }} items found."
```

## 🔧 **Option 3: SMS Gateway Service**

### **Use Your Existing SMS Gateway:**

1. **Deploy SMS Gateway** (separate Pi):
```bash
cd raspberry-pi-sms-gateway
python src/sms_gateway/server.py
```

2. **Add REST notification** to `configuration.yaml`:
```yaml
notify:
  - name: sms_gateway
    platform: rest
    resource: http://192.168.1.100:5000/send_sms
    method: POST_JSON
    headers:
      Content-Type: application/json
    data:
      phone_number: "+1234567890"
      message: "{{ message }}"
```

3. **Add automation:**
```yaml
- id: iphone_gateway_sms
  alias: "iPhone Gateway SMS"
  trigger:
    - platform: state
      entity_id: binary_sensor.apple_store_stock_available
      to: "on"
  action:
    - service: notify.sms_gateway
      data:
        message: "🍎 iPhone available at Apple Store!"
```

## 🎯 **Recommended Setup:**

**For simplicity**: Use **Option 1** (Mobile App)
**For SMS**: Use **Option 2** (Email-to-SMS) - it's free and reliable
**For advanced**: Use **Option 3** (SMS Gateway) if you have SMS modem

## 📱 **Quick Setup - Mobile App:**

1. Install "Home Assistant" app on your phone
2. Add the automation above
3. Replace `YOUR_PHONE_NAME` with your device name from HA
4. Done! You'll get push notifications when stock is found.