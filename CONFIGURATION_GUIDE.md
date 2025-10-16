# 📱 Configuration Guide

## How to Change Phone Number and Store Location

### 1. **Phone Number Configuration**

Edit `config_enhanced.toml` and update the `[sms]` section:

```toml
[sms]
enabled = true
phone_number = "1234567890"        # Your 10-digit phone number (no spaces or dashes)
carrier = "verizon"                # Your carrier (see list below)
email = "your-email@gmail.com"     # Your Gmail address
email_password = "your-app-password"  # Gmail app password (see setup below)
```

### 2. **Store Location Configuration**

Edit `config_enhanced.toml` and update the `[search]` section:

```toml
[search]
device_family = "iphone17pro"     # Don't change this
models = ["MG7Q4LL/A"]            # iPhone model (don't change unless you want different model)
carriers = ["UNLOCKED/US"]        # Carrier preference
country_code = "us"               # Country code
zip_code = "97223"                # Your ZIP code for store search
stores = ["Washington Square"]    # Store names (auto-mapped to store IDs)
```

### 3. **Supported Carriers for SMS**

Choose your carrier from this list:

- **Verizon**: `verizon`
- **AT&T**: `att`
- **T-Mobile**: `tmobile`
- **Sprint**: `sprint`
- **Boost Mobile**: `boost`
- **Cricket**: `cricket`
- **MetroPCS**: `metropcs`
- **US Cellular**: `uscellular`
- **Virgin Mobile**: `virgin`

### 4. **Gmail App Password Setup**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `email_password` field

### 5. **Store Names You Can Use**

Instead of store IDs, just use store names:

- **"Washington Square"** → Apple Washington Square, Tigard, OR
- **"Pioneer Place"** → Apple Pioneer Place, Portland, OR
- **"Tacoma Mall"** → Apple Tacoma Mall, Tacoma, WA
- **"Southcenter"** → Apple Southcenter, Tukwila, WA
- **"Bellevue Square"** → Apple Bellevue Square, Bellevue, WA
- **"University Village"** → Apple University Village, Seattle, WA
- **"Alderwood"** → Apple Alderwood, Lynnwood, WA
- **"Bridgeport Village"** → Apple Bridgeport Village, Tigard, OR

### 6. **Example Configuration**

Here's a complete example for someone in Portland, OR:

```toml
[search]
device_family = "iphone17pro"
models = ["MG7Q4LL/A"]
carriers = ["UNLOCKED/US"]
country_code = "us"
zip_code = "97201"                    # Portland ZIP
stores = ["Washington Square", "Pioneer Place"]  # Multiple stores

[general]
polling_interval_seconds = 1800
report_after_n_counts = 30
data_path = "data.csv"
log_path = "log.txt"
randomize_proxies = false

[sms]
enabled = true
phone_number = "5035551234"           # Your phone number
carrier = "verizon"                   # Your carrier
email = "yourname@gmail.com"          # Your Gmail
email_password = "abcd efgh ijkl mnop"  # Gmail app password
```

### 7. **How to Run**

After configuring:

```bash
# Test single check
poetry run python run_monitor.py check

# Start continuous monitoring
poetry run python run_monitor.py monitor
```

### 8. **Troubleshooting**

- **Store not found**: Try different store name variations
- **SMS not working**: Check Gmail app password and carrier
- **No notifications**: Make sure `enabled = true` in SMS section
- **Wrong store**: Check ZIP code and store name spelling

---

**That's it! The system will automatically map store names to store IDs and send you SMS notifications when your iPhone becomes available.**
