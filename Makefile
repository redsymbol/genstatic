PYTHON=python2.6
clean:
	rm -f $$(find . -name '*.pyc' -o -name '*~')
test:
	$(PYTHON) tests/test_main.py
	cd tests; ./end-to-end-tests.sh