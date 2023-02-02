# CLI client for Vikunja

This is a simple cli for Vikunja, written in python.

It provides a command line interface for adding, viewing and editing todo tasks on a Vikunja Server in order to support
a command line based workflow ~ similar to taskwarrior.
> [The todo app to organize your life.](https://vikunja.io/)

## Installation

- Create a configuration file $HOME/.vjacli/vja.rc with the following contents
  ```shell
  [application]
  frontend_url=https://try.vikunja.io/
  api_url=https://try.vikunja.io/api/v1
  ```
  (If you cloned from git, you may copy the folder .vjacli to your `$HOME` directory instead.)
- Adjust to your needs. `frontend_url` and `api_url` must point to your Vikunja server.
- Install from pypi:
  ```shell
  pip install vja
  vja --help
  ```

## Usage
```shell
vja --help
vja ls
```
(You will be prompted for your account on first usage and any time the access token expires.)

**More on [Features.md](Features.md)**

## Development

### Prepare python virtual environment

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Local build

Build, install and perform some integration-test. For integration test a real Vikunja instance is launched locally via
docker-compose.

```shell
pip install -r requirements_dev.txt
pip uninstall -y vja;rm -rf build dist vja.egg-info; python setup.py sdist bdist_wheel; pip install dist/*.whl;
test/integration/run.sh start test/integration/docker-compose.yml
```

Upload to pypi

```shell
pip uninstall -y vja; rm -rf build dist vja.egg-info; python setup.py sdist bdist_wheel;twine upload dist/*
pip install vja -U
```

