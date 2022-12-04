#!/bin/zsh

python3 -m venv venv;
source venv/bin/activate;
python3 -m pip install -r requirements.txt;
python3 -m pip install pytest-cov
python3 -m pytest --cov=./ --cov-report=html
open htmlcov/index.html

deactivate;
