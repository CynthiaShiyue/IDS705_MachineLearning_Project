VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: all

# Create virtual environment
$(VENV_DIR)/bin/activate:
	
# Install dependencies
install: 
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirement.txt
# #
# # Run the main script
# run:
# 	$(PYTHON) main.py

# all: install run