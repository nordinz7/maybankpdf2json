test:
	python3 -m unittest discover -s tests

release:
	pip install build
	rm -rf dist
	python3 -m build
	python3 -m twine upload dist/* --verbose
