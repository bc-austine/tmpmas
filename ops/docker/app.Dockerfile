# =============================================================================
# TMPMAS Application Container
# =============================================================================
# Development environment container. Includes Python 3.12, project tooling,
# and pre-commit hooks. Used by ops/compose/docker-compose.yml.
# =============================================================================

FROM python:3.12-slim

# Don't write .pyc files; don't buffer stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=5

# System packages required by common Python scientific dependencies.
# Kept minimal — add more only when a dependency requires it.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Working directory inside the container. Bind-mounted from the host repo
# so edits on the host appear instantly in the container.
WORKDIR /app

# Install development tooling first (before copying source) so that
# dependency changes don't invalidate the source layers of the cache.
RUN pip install \
        pytest==8.3.3 \
        pytest-cov==6.0.0 \
        mypy==1.13.0 \
        pre-commit==4.0.1 \
        detect-secrets==1.5.0

# Pre-commit needs git config to install hooks; skip in container
# (hooks run on the host, not in the container).

# ruff is a large binary wheel — separate layer so a failed download
# doesn't force reinstalling everything above.
RUN pip install ruff==0.7.1

# Default command: interactive shell. Overridden per-invocation as needed.
CMD ["bash"]
