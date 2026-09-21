# `ops/dns/` — DNS Blocklist Server

A dnsmasq-based container that resolves prohibited betting domains to
`0.0.0.0`. The `app` and `worker` containers use this as their sole DNS
resolver, enforcing ADR-019 at the network layer.

## How it works

1. On startup, `generate-config.py` reads `/etc/tmpmas/betting-domains.yaml`
   (bind-mounted from `ops/network/`).
2. For every pattern in `write_prohibited_patterns`, a `address=/<domain>/0.0.0.0`
   line is emitted into `/etc/dnsmasq.d/blocked.conf`.
3. dnsmasq runs in the foreground and answers queries.
4. Blocked domains resolve to `0.0.0.0` (null route, fails fast).
5. Other domains are forwarded to Cloudflare (1.1.1.1) and Google (8.8.8.8).
6. Every query is logged for observability.

## Adding a blocked domain

Edit `ops/network/betting-domains.yaml`. Append a pattern under
`write_prohibited_patterns` in the shape:

```yaml
- pattern: '(^|\.)new-betting-site\.com$'
```

Restart the DNS container:

```bash
docker compose -f ops/compose/docker-compose.yml restart blocklist-dns
```

## Verifying the block is active

From the host:

```bash
docker compose -f ops/compose/docker-compose.yml exec app \
    python -c "import socket; print(socket.gethostbyname('bet365.com'))"
```

**Expected:** `0.0.0.0`

If this returns a real IP, the DNS resolver isn't being used — check
`docker compose ps` and the `app` service's `dns:` setting.

## Limitations

- **IP-hardcoded traffic bypasses this block.** Only hostname-based traffic
  is affected. The CI outbound-API pattern gate (stage 15) blocks hardcoded
  domains and IPs at the code level.
- **Upstream DNS is public.** If we later require query privacy, swap
  Cloudflare for a self-hosted recursive resolver.
- **No HTTPS/SVCB enforcement.** A malicious resolver upstream could serve
  AAAA records for blocked domains, but the block takes precedence.

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Alpine + dnsmasq + python3 |
| `generate-config.py` | YAML → dnsmasq config |
| `entrypoint.sh` | Startup orchestration |
| `README.md` | This file |
