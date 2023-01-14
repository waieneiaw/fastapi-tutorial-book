#------------------------------------------------------------------------------
# Makefile
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# vars
APP_NAME := blog

#------------------------------------------------------------------------------
.PHONY: help
## Help commnad
help:
	@cat $(MAKEFILE_LIST) | \
		python -u -c \
			'import sys; \
			import re; from itertools import tee,chain; \
			rx = re.compile(r"^[a-zA-Z0-9\-_]+:"); \
			xs, ys = tee(sys.stdin); \
			xs = chain([""], xs); \
			[print(f"""\x1b[36m{line.split(":", 1)[0]:20s}\x1b[0m\t{prev.lstrip("# ").rstrip() if prev.startswith("##") else "" }""") for prev, line in zip(xs, ys) if rx.search(line)]'

#------------------------------------------------------------------------------
.PHONY: setup
## Setup python local environment (need `poetry`)
setup:
	@rm -rf .venv
	@python -m venv .venv
	@pip install --upgrade pip
	@poetry install
	@poetry shell

#------------------------------------------------------------------------------
.PHONY: run
## Run
run:
	poetry run uvicorn $(APP_NAME).main:app --reload

#------------------------------------------------------------------------------
.PHONY: test
## Test
test:
	poetry run python -m pytest . -v --tb=short -l

#------------------------------------------------------------------------------
.PHONE: tox
## Run tox
tox:
	@tox
