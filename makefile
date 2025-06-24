.PHONY: lint fmt mypy all terraform_init terraform_plan terraform_apply
# === Ruff ===

lint:
	poetry run ruff check

fmt:
	poetry run ruff check --fix

all: fmt lint

# === terraform ===

terraform_init:
	cd terraform && terraform init

terraform_plan:
	cd terraform && terraform plan

terraform_apply:
	cd terraform && terraform apply $(args)