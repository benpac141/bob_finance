.PHONY: help install clean run analysis report all

# Variables
PYTHON := python
VENV := venv
SRC := src

help:
	@echo "Commandes disponibles:"
	@echo "  make install    - Installer les dépendances"
	@echo "  make clean      - Nettoyer les fichiers temporaires"
	@echo "  make run        - Exécuter l'analyse complète"
	@echo "  make analysis   - Exécuter uniquement l'analyse"
	@echo "  make report     - Générer uniquement le rapport"
	@echo "  make all        - Tout exécuter (installation + analyse)"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf outputs/figures/*
	rm -rf outputs/reports/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

run:
	$(PYTHON) $(SRC)/cli.py run --config config.yaml

analysis:
	$(PYTHON) $(SRC)/cli.py analyze --config config.yaml

report:
	$(PYTHON) $(SRC)/cli.py report --config config.yaml

all: install run

