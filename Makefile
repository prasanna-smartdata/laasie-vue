.PHONY: ensure_venv
ensure_venv:
	cd api && python3 -m venv venv

.PHONY: ensure_api
ensure_api: ensure_venv
	cd api && . ./venv/bin/activate && pip install -r requirements.txt

.PHONY: ensure_api_win
ensure_api_win: ensure_venv
	cd api && powershell .\venv\bin\Activate.ps1 && pip install -r requirements.txt

.PHONY: ensure_ui
ensure_ui:
	cd ui && npm ci

.PHONY: ensure
ensure: ensure_ui ensure_api

.PHONY: build_ui
build_ui:
	npm run --prefix=ui build

.PHONY: build
build: build_ui

.PHONY: lint_api
lint_api:
	cd api && . ./venv/bin/activate && pylint . && mypy .

.PHONY: lint_ui
lint_ui:
	cd ui && npm run lint

.PHONY: lint
lint: lint_api lint_ui

.PHONY: run_api
run_api: build
	@echo "******"
	@echo "Running script as sudo. You may be prompted to enter the password..."
	@echo "******"
	sudo ./scripts/start-api.sh

.PHONY: run_ui
run_ui:
	npm run --prefix=ui dev

.PHONY: api_test
api_test:
	PYTHONPATH=. pytest