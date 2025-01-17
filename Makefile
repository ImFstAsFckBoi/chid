ifeq ($(OS), Windows_NT)
	PY = python
else
	PY = python3
endif

PIP = ${PY} -m pip


CLEAN_LIST = *.so build/ dist/ *.egg-info/ .mypy_cache/ .pytest_cache/

dev:
	${PIP} install -e .

install:
	${PIP} install .

venv:
	${PY} -m venv .venv 

build:
	${PY} -m build --sdist --wheel

test:
	${PY} -m pytest tests/ -W ignore::DeprecationWarning

clean:
	rm -rf ${CLEAN_LIST}

full-clean: clean
	rm -rf .venv/