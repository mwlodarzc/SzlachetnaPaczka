SHELL := /bin/bash
.DEFAULT_GOAL := run
.PHONY: run clean venv

setup: requirements.txt
		source venv/bin/activate
		sudo apt-get install postgresql postgresql-contrib
		pip install -r requirements.txt

run: venv setup
		sudo systemctl start postgresql.service
		python3 src/app.py

clean:
		rm -rf src/__pycache__