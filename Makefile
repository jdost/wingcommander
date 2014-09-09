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

publish:
	python setup.py register
	python setup.py sdist upload --sign --identity=2073CDA5

shell:
	${PYTHONPATH} python
