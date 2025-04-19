rm -rf .publish
rm -rf dist
rm -rf *.egg-info
rm -rf build
rm -rf .pytest_cache

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
rm -rf .publish

git add .
git commit -m "Publish to PyPI"
git push origin main
version=$(python setup.py --version)
git tag -a v$version -m "Release version $version"
git push origin v$version
git push --tags
