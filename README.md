# 🍎 Apple Store Stock Monitor

**API-based Apple product stock monitoring with no hardcoded data**

Monitor any Apple product at any Apple store with real-time availability checking, individual product tracking, and Home Assistant integration.

## ✨ Features

- **🔍 Dynamic Product Discovery** - Automatically finds all Apple products via API
- **🏪 Dynamic Store Discovery** - Finds Apple stores near any zipcode
- **📱 Individual Tracking** - Each product/store combination tracked separately
- **🏠 Home Assistant Integration** - Individual sensors for each product
- **🔮 Smart Predictions** - Learns restock patterns over time
- **📲 Multiple Notifications** - SMS, email, Home Assistant alerts

## 🚀 Quick Start

### 1. Setup
```bash
python setup.py
```

### 2. Find Your iPhone
```bash
# Search for iPhone 17 Pro models
python apple_monitor.py discover "iPhone 17 Pro"

# Add the one you want (example)
python apple_monitor.py add-product MG7Q4LL/A "iPhone 17 Pro 512GB Deep Blue"
```

### 3. Find Nearby Stores
```bash
# Find stores near you
python apple_monitor.py stores 97223

# Add stores you want to monitor
python apple_monitor.py add-store R090 "Washington Square, Tigard"
```

### 4. Start Monitoring
```bash
# Check once
python apple_monitor.py check

# Continuous monitoring
python apple_monitor.py run
```

## 📱 iPhone 17 Pro Deep Blue 512GB

**Product Code**: `MG7Q4LL/A`  
**Quick Setup**: `python setup.py` → Choose option 1

## 🏠 Home Assistant Integration

### Install Integration
```bash
cp -r custom_components/apple_store_notifier /config/custom_components/
```

### Generate Dashboard
```bash
python generate_ha_dashboard.py
```

### Individual Sensors
Each product/store gets its own sensor:
- `sensor.iphone_17_pro_512gb_deep_blue_at_washington_square_tigard`
- `sensor.iphone_17_pro_512gb_deep_blue_at_pioneer_place_portland`

## 🔧 Commands

```bash
python apple_monitor.py discover <search>    # Find products
python apple_monitor.py stores <zipcode>     # Find stores  
python apple_monitor.py add-product <code> <name>  # Add product
python apple_monitor.py add-store <code> <name>    # Add store
python apple_monitor.py check                # Check stock once
python apple_monitor.py run                  # Continuous monitoring
python apple_monitor.py status               # Show configuration
```

## 📊 No Hardcoded Data

- ✅ **Products**: Discovered dynamically from Apple's API
- ✅ **Stores**: Discovered by zipcode via Apple's API  
- ✅ **Availability**: Real-time API checks
- ✅ **Predictions**: Based on learned patterns

## 🎯 Perfect For

- **iPhone 17 Pro Deep Blue 512GB** monitoring (tested and working)
- **Any Apple product** (iPhones, iPads, Macs, Apple Watch, AirPods)
- **Multiple products** across multiple stores
- **Home Assistant** users wanting individual product sensors
- **Restock predictions** based on historical patterns

## 📁 Core Files

- `apple_monitor.py` - Main monitoring script
- `dynamic_apple_monitor.py` - API-based product/store discovery
- `flexible_config_system.py` - Configuration management
- `restock_analyzer.py` - Pattern analysis and predictions
- `custom_components/` - Home Assistant integration

## 🔄 How It Works

1. **Discovery**: Scans Apple's website for current products and stores
2. **Configuration**: You choose which products and stores to monitor
3. **Monitoring**: Checks availability via Apple's pickup API
4. **Learning**: Records patterns to predict future restocks
5. **Alerting**: Notifies you when products become available

---

**No hardcoded product lists. No outdated store data. Just pure API-based intelligence.** 🍎✨