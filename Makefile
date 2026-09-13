PYTHON ?= python

.PHONY: setup build clean

setup:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) scripts/build.py

clean:
	rm -f dist/*.pdf dist/*.html
