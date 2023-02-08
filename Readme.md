# CLI client for Vikunja

This is a simple CLI for Vikunja > [The todo app to organize your life.](https://vikunja.io/)

It provides a command line interface for adding, viewing and editing todo tasks on a Vikunja Server.
The goal is to support a command line based task workflow ~ similar to taskwarrior.

## Installation

- Install from pypi:
  ```shell
  pip install vja
  vja --help
  ```
- Upgrade existing version:
  ```shell
  pip install vja --upgrade
  ```

## Configuration

Before using vja you must provide a configuration.

- Create a configuration file $HOME/.vjacli/vja.rc with ~ the following contents
  ```shell
  [application]
  frontend_url=https://try.vikunja.io/
  api_url=https://try.vikunja.io/api/v1
  ```
  (If you cloned from git, you may copy the folder .vjacli to your `$HOME` directory instead.)
- Adjust to your needs.  
  `frontend_url` and `api_url` must point to your own Vikunja server.  
  Especially the api_url must be reachable from your client. This can be verified for example
  by  `curl https://mydomain.com/api/v1/info`

## Usage

```shell
vja --help
vja ls
```

(You will be prompted for your account on first usage and any time the access token expires.)

**More documentation is available on [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md)**

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
```

Run integration test (requires docker and docker-compose)

```shell
test/integration/run.sh start localhost test/integration/docker-compose.yml
test/integration/run.sh test
test/integration/run.sh stop localhost test/integration/docker-compose.yml
```

