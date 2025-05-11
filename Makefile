# Variables
PYTHON = python3
PIP = pip
TEST_CMD = $(PYTHON) -m unittest discover -s tests

.PHONY: test release install clean help

test:
	$(TEST_CMD)

install:
	$(PIP) install -r requirements.txt

clean:
	rm -rf dist maybankpdf2json.egg-info __pycache__ */__pycache__ *.pyc *.pyo

release: install clean
	$(PIP) install build twine
	$(PYTHON) -m build
	$(TEST_CMD)
	if [ $$? -eq 0 ]; then \
	  $(PYTHON) -m twine upload dist/* --verbose; \
	else \
	  echo "Tests failed. Aborting upload."; \
	  exit 1; \
	fi

help:
	@echo "Available targets:"
	@echo "  test     - Run unit tests"
	@echo "  install  - Install dependencies from requirements.txt"
	@echo "  clean    - Remove build and Python cache artifacts"
	@echo "  release  - Build, test, and upload the package to PyPI"
	@echo "  help     - Show this help message"
