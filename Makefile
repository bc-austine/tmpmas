# =============================================================================
# TMPMAS — Developer Command Shortcuts
# =============================================================================
# Wraps docker compose commands so developers don't have to remember long
# paths. See CONTRIBUTING.md for full context.
#
# Usage:
#     make help         Show available targets
#     make up           Start the environment
#     make shell        Open a shell inside the app container
#     make test         Run tests in the container
# =============================================================================

COMPOSE_FILE := ops/compose/docker-compose.yml
COMPOSE      := docker compose -f $(COMPOSE_FILE)

.DEFAULT_GOAL := help
.PHONY: help up down restart shell logs test lint format clean ps rebuild check

help: ## Show this help message
	@echo "TMPMAS developer targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

up: ## Start the environment (app + db) in the background
	$(COMPOSE) up -d
	@echo ""
	@echo "Environment is up. Use 'make shell' to open a shell inside the app container."

down: ## Stop the environment (preserves the database volume)
	$(COMPOSE) down

restart: ## Restart the app container
	$(COMPOSE) restart app

rebuild: ## Rebuild the app container image and restart
	$(COMPOSE) build --no-cache app
	$(COMPOSE) up -d app

shell: ## Open a bash shell inside the app container
	$(COMPOSE) exec app bash

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

ps: ## Show running containers
	$(COMPOSE) ps

test: ## Run the test suite inside the app container
	$(COMPOSE) exec app pytest

lint: ## Run ruff lint inside the app container
	$(COMPOSE) exec app ruff check src tests

format: ## Run ruff format inside the app container
	$(COMPOSE) exec app ruff format src tests

check: ## Run pre-commit against all files inside the app container
	$(COMPOSE) exec app pre-commit run --all-files

clean: ## Stop the environment AND delete the database volume
	@echo "WARNING: This deletes the local database. Continue? [y/N] " && read ans && [ "$$ans" = "y" ]
	$(COMPOSE) down -v
