python3 -m venv .publish
source .publish/bin/activate
pip install setuptools wheel twine build
python -m build
python -m twine upload dist/*
deactivate
rm -rf .venv
rm -rf dist
rm -rf *.egg-info
rm -rf build
rm -rf .pytest_cache
