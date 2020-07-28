CWD     = $(CURDIR)
MODULE  = $(shell echo $(notdir $(CWD)) | tr "[:upper:]" "[:lower:]" )
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3

.PHONY: all
all: py

py: $(PY) $(MODULE).py

.PHONY: install update

install: $(PIP) $(NIMBLE) js
	-$(MAKE) $(OS)_install
	$(PIP)   install    -r requirements.txt
update: $(PIP)
	-$(MAKE) $(OS)_update
	$(PIP)   install -U    pip
	$(PIP)   install -U -r requirements.txt
	$(MAKE)  requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
	$(MAKE) requirements.txt
