PYTHONVERSION = $(shell python --version 2>&1 | sed 's/Python //g')
PYTHONMAJOR = $(firstword $(subst ., ,${PYTHONVERSION}))

ifeq "${PYTHONMAJOR}" "2"
	NOSEOPTS = --with-color
else
	NOSEOPTS =
endif

init:
	pip install -r requirements.txt

unittest:
	nosetests ${NOSEOPTS} ./tests/test_*.py

lint:
	flake8 --ignore=F401 --max-complexity 12 src/
	flake8 --ignore=F401 --max-complexity 12 tests/

test: lint unittest

clean:
	rm -f ./src/wincommander/*.pyc
	rm -f ./src/wingcommander/util/*.pyc
	rm -f ./tests/*.pyc
