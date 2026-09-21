# =============================================================================
# TMPMAS — DNS Blocklist Server
# =============================================================================
# Runs dnsmasq with a generated config that resolves prohibited betting
# domains to 0.0.0.0. Used by the app container as its sole DNS resolver.
#
# Base image: python:3.12-slim (Debian) rather than alpine because the
# Alpine python3 + py3-yaml chain pulls ~22 packages, several of which
# failed to download on this network. Debian gives us Python pre-installed;
# we only add dnsmasq.
# =============================================================================

FROM python:3.12-slim

# Only package we need beyond Python itself.
RUN apt-get update \
    && apt-get install -y --no-install-recommends dnsmasq \
    && rm -rf /var/lib/apt/lists/*

# PyYAML is the only Python dependency for the config generator.
RUN pip install --no-cache-dir pyyaml==6.0.2

COPY generate-config.py /usr/local/bin/generate-config.py
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# DNS uses UDP/53 primarily, TCP/53 for large responses.
EXPOSE 53/udp 53/tcp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
