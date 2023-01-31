#!/bin/bash
set -euo pipefail

pip install -r requirements_dev.txt
pip uninstall -y vja
python setup.py sdist bdist_wheel
pip install dist/*.whl
