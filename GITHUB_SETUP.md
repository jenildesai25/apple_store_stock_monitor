# GitHub + HACS Setup Guide

## Step 1: Push to GitHub

1. **Create GitHub Repository**:
   ```bash
   # Initialize git (if not already done)
   git init
   git add .
   git commit -m "Initial commit: Apple Store Stock Notifier for Home Assistant"
   
   # Create repo on GitHub, then:
   git remote add origin https://github.com/jenil/apple-store-stock-notifier.git
   git branch -M main
   git push -u origin main
   ```

2. **Repository Structure** (what HACS expects):
   ```
   apple-store-stock-notifier/
   ├── custom_components/
   │   └── apple_store_notifier/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── apple_monitor.py
   │       ├── sensor.py
   │       └── binary_sensor.py
   ├── hacs.json
   ├── README.md
   └── info.md
   ```

## Step 2: Install via HACS

### Option A: Add as Custom Repository

1. **In Home Assistant**:
   - Go to HACS → Integrations
   - Click three dots (⋮) → Custom repositories
   - Add: `https://github.com/jenil/apple-store-stock-notifier`
   - Category: Integration
   - Click "Add"

2. **Install**:
   - Find "Apple Store Stock Notifier" in HACS
   - Click "Download"
   - Restart Home Assistant

### Option B: Submit to HACS Default (Future)

Once tested, you can submit to HACS default repositories:
- Fork https://github.com/hacs/default
- Add your repo to `integration.json`
- Submit PR

## Step 3: Configure Integration

1. **Add Integration**:
   - Settings → Devices & Services
   - Add Integration → "Apple Store Stock Notifier"

2. **Configuration**:
   - SMS Gateway URL: `http://192.168.1.100:5000`
   - Check Interval: 5 minutes
   - Select stores and products

## Step 4: Deploy SMS Gateway (Separate)

The SMS gateway runs separately:

```bash
# On your SMS gateway Pi
git clone https://github.com/jenil/apple-store-stock-notifier.git
cd apple-store-stock-notifier/raspberry-pi-sms-gateway
pip install -r requirements.txt
python src/sms_gateway/server.py
```

## Benefits of GitHub + HACS:

✅ **Easy Installation**: One-click install via HACS  
✅ **Automatic Updates**: HACS handles updates  
✅ **Version Control**: Track changes and releases  
✅ **Community**: Others can use and contribute  
✅ **Professional**: Standard Home Assistant integration approach

## Repository URL:
`https://github.com/jenil/apple-store-stock-notifier`

## HACS Installation URL:
Add this as a custom repository in HACS.