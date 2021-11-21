SHELL:=/bin/bash
POETRY=$(shell command -v poetry | cut -d '/' -f 6)
VENV=$(shell ls -la | grep '.venv' | cut -d ' ' -f 15)


.PHONY: install
install:
	@echo "Installing poetry..."
	[ $(POETRY) == "poetry" ] && $(SHELL) -c "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -"
	@echo "Done."
	@echo "Installing dependencies..."
	[ $(VENV) == ".venv" ] && $(SHELL) -c "poetry install"


run:
	@echo "Rendering..."
	$(SHELL) -c "poetry run python app.py"
	@echo "Done."

test:
	@poetry run pytest -vv

.PHONY: clean
clean:
	@echo "Cleaning HTML files..."
	find . -name "*.html" -not -path "./templates/*" -exec rm -f {} \;
	@echo "Cleaning PYC files..."
	find . -name "*.pyc" -exec rm -f {} \;
	@echo "Done."

