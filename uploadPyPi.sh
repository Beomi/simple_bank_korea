rm -rf build
rm -rf dist
rm -rf simple_bank_korea.egg-info
python setup.py sdist upload -r pypi
