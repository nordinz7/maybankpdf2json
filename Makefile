# Variables
PYTHON = python3
PIP = pip
TEST_CMD = $(PYTHON) -m unittest discover -s tests -v

.PHONY: test release install clean bump patch publish help

test:
	$(TEST_CMD)

install:
	$(PIP) install -r requirements.txt

clean:
	rm -rf dist maybankpdf2json.egg-info __pycache__ */__pycache__ *.pyc *.pyo

# Usage: make bump VERSION=0.1.53
bump:
	@[ -n "$(VERSION)" ] || (echo "Usage: make bump VERSION=x.y.z" && exit 1)
	sed -i '' 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
	sed -i '' 's/    version=".*"/    version="$(VERSION)"/' setup.py
	@echo "Bumped version to $(VERSION)"

# Auto-increment the patch version (0.1.52 -> 0.1.53)
patch:
	$(eval NEW_VERSION := $(shell $(PYTHON) -c "import re,pathlib; v=re.search(r'version = \"(\d+\.\d+\.)(\d+)\"', pathlib.Path('pyproject.toml').read_text()); print(v.group(1)+str(int(v.group(2))+1))"))
	sed -i '' 's/^version = .*/version = "$(NEW_VERSION)"/' pyproject.toml
	sed -i '' 's/    version=".*"/    version="$(NEW_VERSION)"/' setup.py
	@echo "Patch bumped to $(NEW_VERSION)"

# Bump patch, commit, tag and push to trigger the CI publish workflow
publish:
	$(eval NEW_VERSION := $(shell $(PYTHON) -c "import re,pathlib; v=re.search(r'version = \"(\d+\.\d+\.)(\d+)\"', pathlib.Path('pyproject.toml').read_text()); print(v.group(1)+str(int(v.group(2))+1))"))
	sed -i '' 's/^version = .*/version = "$(NEW_VERSION)"/' pyproject.toml
	sed -i '' 's/    version=".*"/    version="$(NEW_VERSION)"/' setup.py
	@echo "Bumped to $(NEW_VERSION)"
	git add pyproject.toml setup.py
	git commit -m "chore: release v$(NEW_VERSION)"
	git tag v$(NEW_VERSION)
	git push && git push --tags
	@echo "Tagged v$(NEW_VERSION) — GitHub Actions will publish to PyPI"

release: clean install
	$(PIP) install build twine
	$(TEST_CMD)
	$(PYTHON) -m build
	$(PYTHON) -m twine upload dist/* --verbose

help:
	@echo "Available targets:"
	@echo "  test              - Run unit tests with verbose output"
	@echo "  install           - Install dependencies from requirements.txt"
	@echo "  clean             - Remove build and Python cache artifacts"
	@echo "  bump VERSION=x.y.z - Manually set version in pyproject.toml and setup.py"
	@echo "  patch             - Auto-increment patch version (e.g. 0.1.52 -> 0.1.53)"
	@echo "  publish           - Bump patch, commit, tag and push to trigger CI publish"
	@echo "  release           - Build, test, and upload the package to PyPI (local)"
	@echo "  help              - Show this help message"
