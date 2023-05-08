SHELL := /bin/bash
.DEFAULT_GOAL := run
.PHONY: run clean venv

setup: requirements.txt
		sudo apt-get install postgresql-12 postgresql-contrib-12 postgresql-client-12 postgresql-server-dev-12
		export PGCluster=12/main
		pip install -r requirements.txt

run: venv setup
		python3 src/app.py

clean:
		rm -rf src/__pycache__