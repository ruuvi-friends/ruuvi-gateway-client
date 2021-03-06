# Developer Notes

## Execute tests

```sh
python -m venv .venv
source .venv/bin/activate
python -n pip install pytest
pytest
```

## Build and release

https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives

```sh
python -m build
```

### Test in testpypi

Upload to test pypi to verify that descriptions etc. are correct

https://test.pypi.org/project/ruuvitag-sensor/

https://twine.readthedocs.io/en/stable/#using-twine
```sh
$ twine upload -r testpypi dist/*
```

### Release a new version

1. Update version from setup.cfg and CHANGELOG and push to main 
2. Update Tags
```sh
$ git tag x.x.x
$ git push origin --tags
```
3. Upload new version to pypi
```
$ twine upload dist/*
```
