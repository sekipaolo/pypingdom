# Minimal makefile
#


.PHONY: publish
publish:
	@echo "make clean"
	@echo "python setup.py sdist bdist_wheel"
	@echo "twine"

.PHONY: clean
clean:
	@echo "Cleaning up distutils and tox stuff"
	rm -rf build dist deb_dist
	rm -rf *.egg .eggs *.egg-info
	rm -rf .tox
	@echo "Cleaning up byte compiled python stuff"
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete

.PHONY: tests
tests:
	python testing/manualtest_check.py
