#!/bin/zsh

python3 -m venv venv;
source venv/bin/activate;
python3 -m pip install -r requirements.txt;
python3 -m pip install coverage;
python3 -m coverage run -m pytest;
coverage html;
open htmlcov/index.html;
deactivate;
