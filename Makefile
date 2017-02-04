.PHONY: publish clean

publish:
	@echo "Releasing package..."
	@rm -rf build dist *.egg-info
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@echo "Don't forget to 'make clean'"

clean:
	@echo "Cleaning up files..."
	@rm -rf build dist *.egg-info *.pyc

