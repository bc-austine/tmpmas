#!/usr/bin/env sh
# Entrypoint for the DNS blocklist container.

set -e

echo "[dns] Generating blocklist config..."
python3 /usr/local/bin/generate-config.py

echo "[dns] Starting dnsmasq (foreground)..."
exec dnsmasq \
    --no-daemon \
    --keep-in-foreground \
    --conf-file=/dev/null \
    --conf-dir=/etc/dnsmasq.d \
    --log-queries \
    --log-facility=-
