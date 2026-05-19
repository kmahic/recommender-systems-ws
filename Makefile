.PHONY: help setup data notebooks slides lab clean all reset

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies with uv
	uv sync

data: ## Download ML-25M and create sampled subset
	uv run python data/sample_ml25m.py

notebooks: ## Re-generate notebook .ipynb files
	uv run python _gen_new_nbs.py

slides: ## Render Marp slide deck to HTML
	npx @marp-team/marp-cli slides/slides.md -o slides/slides.html --allow-local-files

lab: ## Launch JupyterLab
	uv run jupyter lab --notebook-dir=notebooks

clean: ## Remove downloaded data, outputs, and rendered slides
	rm -rf data/ml-25m data/ml-25m-sample
	rm -f outputs/*.json outputs/*.csv outputs/*.png
	rm -f slides/*.html

reset: clean ## Full reset (clean + remove uv lockfile)
	rm -rf .venv uv.lock

all: setup data notebooks slides ## One-command full setup
	@echo "\n✅ Setup complete. Run 'make lab' to start."

