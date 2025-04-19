
git add .
git commit -m "Publish to PyPI"
git push origin main
version=$(python setup.py --version)
git tag -a v$version -m "Release version $version"
git push origin v$version
git push --tags
