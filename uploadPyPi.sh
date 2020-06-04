rm -rf build
rm -rf dist
rm -rf simple_bank_korea.egg-info
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
