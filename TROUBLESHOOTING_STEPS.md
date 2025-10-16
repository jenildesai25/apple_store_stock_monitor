# Troubleshooting Steps for Apple Store Integration

## 🔍 **Step 1: Check Integration Status**

1. **Settings** → **Devices & Services**
2. **Look for "Apple Store Stock Notifier"** or similar
3. **Check if it shows:**
   - ✅ **Configured** (good)
   - ❌ **Failed to load** (needs fixing)
   - ⚠️ **In Repairs** (needs attention)

## 🔍 **Step 2: Find Your Entities**

1. **Developer Tools** → **States**
2. **Search for**: `apple`, `iphone`, or `stock`
3. **Look for entities like:**
   - `sensor.apple_store_*`
   - `sensor.iphone_*`
   - `binary_sensor.apple_store_*`
   - `binary_sensor.iphone_*`

## 🔍 **Step 3: Check Logs**

1. **Settings** → **System** → **Logs**
2. **Search for**: `apple_store_notifier`
3. **Look for errors** (red text)

## 🛠️ **Step 4: Create Working Card**

Once you find your entities, use this template:

```yaml
type: entities
title: 📱 iPhone Stock Monitor
entities:
  - entity: [YOUR_MAIN_SENSOR_NAME]
    name: Items Available
  - entity: [YOUR_BINARY_SENSOR_NAME] 
    name: Stock Found
  - entity: [YOUR_LAST_CHECK_SENSOR_NAME]
    name: Last Check
show_header_toggle: false
```

## 🔄 **Step 5: If Nothing Shows Up**

The integration might not be loaded. Try:

1. **Restart Home Assistant**
2. **Check HACS** → Make sure integration is installed
3. **Re-add Integration** if needed

## 📋 **Common Entity Names to Try:**

- `sensor.apple_store_stock_available`
- `sensor.iphone_monitor_status`
- `binary_sensor.apple_store_stock_available`
- `binary_sensor.iphone_stock_found`
- `sensor.apple_store_last_check`

## 🆘 **If Still Not Working:**

Tell me:
1. **What entities do you see** in Developer Tools → States?
2. **What's the integration status** in Devices & Services?
3. **Any errors in the logs?**