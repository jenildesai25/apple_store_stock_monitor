#!/usr/bin/with-contenv bashio

# Get configuration
SMS_GATEWAY_URL=$(bashio::config 'sms_gateway_url')
CHECK_INTERVAL=$(bashio::config 'check_interval')

# Export environment variables
export SMS_GATEWAY_URL
export CHECK_INTERVAL

# Copy application files
cp -r /app/* /data/

# Change to data directory
cd /data

# Start the monitor
bashio::log.info "Starting Apple Store Stock Notifier..."
bashio::log.info "SMS Gateway: ${SMS_GATEWAY_URL}"
bashio::log.info "Check Interval: ${CHECK_INTERVAL} seconds"

python3 run_monitor.py monitor