.PHONY: lint fmt mypy all terraform_init terraform_plan terraform_apply pipeline_run
# === Ruff ===

lint:
	uv run ruff check

fmt:
	uv run ruff check --fix

all: fmt lint

# === Terraform ===

terraform_init:
	cd terraform && terraform init

terraform_plan:
	cd terraform && terraform plan

terraform_apply:
	cd terraform && terraform apply $(args)

# === pipeline ===
pipeline_run:
	python -m pipeline_ph1.pipelines.house_prices_pipeline --enable_cache=$(enable_cache)