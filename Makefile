
dev: ## Development environment
	uv run fastapi dev


test: ## Run tests
	PYTHONPATH=./ uv run pytest
