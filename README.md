# CLI client for Vikunja

This is a simple cli for Vikunja, written in python.
It provides a command line interface ~ similar to taskwarrior.
> [The todo app to organize your life.](https://vikunja.io/)

## Installation

- Copy folder .vjacli to your `$HOME` directory and adjust to your needs.
  `frontend_url` and `api_url` must point to your instance
- Install from pypi;

```shell
pip install vja
vja --help
```

## Usage

see [Features.md](Features.md)

## Development
### Project setup

```shell
rm -rf build dist vja.egg-info; python setup.py sdist bdist_wheel; pip install .
```

### Local build
Build, install and launch some integration-test. For integration test a real Vikunja instance is launched locally via docker-compose.
```shell
pip install -r requirements_dev.txt
pip uninstall -y vja;rm -rf build dist vja.egg-info; python setup.py sdist bdist_wheel; pip install dist/*.whl;
test/integration/run.sh start test/integration/docker-compose.yml
```
Upload to pypi
```shell
twine upload dist/*
pip install vja -U
```

