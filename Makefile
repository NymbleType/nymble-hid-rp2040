.PHONY: test clean

VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install pytest

test: $(VENV)
	$(PYTHON) -m pytest tests/ -v

clean:
	rm -rf $(VENV)