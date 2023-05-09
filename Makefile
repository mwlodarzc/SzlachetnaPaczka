SHELL := /bin/bash
.DEFAULT_GOAL := run
.PHONY: run clean venv

setup: requirements.txt
		source venv/bin/activate
		sudo apt-get install postgresql-15 postgresql-contrib-15 postgresql-client-15 postgresql-server-dev-15
		export PGCluster=15/main
		pip install -r requirements.txt

run: venv setup
		sudo service postgresql start
		python3 src/app.py

clean:
		rm -rf src/__pycache__