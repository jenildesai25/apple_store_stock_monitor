# Simple Dashboard Card Setup

## 📊 **Basic Card (Recommended)**

1. **Edit Dashboard** → **Add Card** → **Entities Card**
2. **Copy and paste this YAML:**

```yaml
type: entities
title: 🍎 Apple Store Monitor
entities:
  - entity: sensor.apple_store_stock_available
    name: Items Available
    icon: mdi:apple
  - entity: binary_sensor.apple_store_stock_available
    name: Stock Found
    icon: mdi:check-circle
  - entity: sensor.apple_store_last_check
    name: Last Check
    icon: mdi:clock-outline
show_header_toggle: false
```

## 📱 **What You'll See:**

```
┌─────────────────────────────────┐
│      🍎 Apple Store Monitor     │
├─────────────────────────────────┤
│ 🍎 Items Available         0    │
│ ✅ Stock Found            Off   │
│ 🕐 Last Check      Oct 16 5:30  │
└─────────────────────────────────┘
```

## 🔍 **To See Your Configuration:**

**Click on "Items Available"** → **Shows attributes:**
- **monitoring_stores**: ["Fifth Avenue", "SoHo"]
- **monitoring_products**: ["iPhone 15 Pro 128GB Natural Titanium", ...]
- **check_interval_minutes**: 10
- **available_items**: [] (or list of available items)

## 📊 **Enhanced Card (Optional)**

If you want to see stores and products directly on the card:

```yaml
type: entities
title: 🍎 Apple Store Monitor
entities:
  - entity: sensor.apple_store_stock_available
    name: Items Available
    icon: mdi:apple
  - entity: sensor.apple_store_last_check
    name: Last Check
    icon: mdi:clock-outline
  - type: section
    label: Configuration
  - type: attribute
    entity: sensor.apple_store_stock_available
    attribute: monitoring_stores
    name: Stores
    icon: mdi:store
  - type: attribute
    entity: sensor.apple_store_stock_available
    attribute: monitoring_products
    name: iPhone Models
    icon: mdi:cellphone
show_header_toggle: false
```

**This shows your stores and iPhone models directly on the dashboard!**