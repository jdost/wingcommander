PYTHONVERSION = $(shell python --version 2>&1 | sed 's/Python //g')
PYTHONMAJOR = $(firstword $(subst ., ,${PYTHONVERSION}))
PYTHONPATH = PYTHONPATH=$(PWD)/src

ifeq "${PYTHONMAJOR}" "2"
	NOSEOPTS = --with-color
else
	NOSEOPTS =
endif

init:
	pip install -r requirements.txt

unittest:
	${PYTHONPATH} nosetests ${NOSEOPTS} ./tests/test_*.py

lint:
	flake8 --ignore=F401 --max-complexity 12 src/
	flake8 --ignore=F401 --max-complexity 12 tests/

test: lint unittest

clean:
	rm -f ./src/wincommander/*.pyc
	rm -f ./src/wingcommander/util/*.pyc
	rm -f ./tests/*.pyc

clean-build:
	rm -rf ./build/
	rm -rf ./dist/
	rm -rf *.egg-info

clean-all: clean clean-build

shell:
	${PYTHONPATH} python

publish:
	python setup.py register
	python setup.py sdist upload --sign --identity=2073CDA5
	python setup.py bdist_wheel upload --sign --indentity=2073CDA5

docs-init:
	pip install -r docs/requirements.txt

docs: docs-init
	cd docs && make html

docs-serve:
	cd docs/build/html/ && python -m SimpleHTTPServer 8080

docs-publish: clean docs
	git co gh-pages
	mv docs/build/html/* .
	git commit -a
	git push
