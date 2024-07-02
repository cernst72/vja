# CLI client for Vikunja

[![pypi package version](https://img.shields.io/pypi/v/vja)](https://pypi.org/project/vja/)
[![pypi downloads](https://img.shields.io/pypi/dw/vja)](https://pypi.org/project/vja/)
[![pipeline status](https://gitlab.com/ce72/vja/badges/main/pipeline.svg)](https://gitlab.com/ce72/vja/-/pipelines)
[![coverage report](https://gitlab.com/ce72/vja/badges/main/coverage.svg)](https://gitlab.com/ce72/vja/commits/main)

This is a simple CLI for Vikunja > [The todo app to organize your life.](https://vikunja.io/)

It provides a command line interface for adding, viewing and editing todo tasks on a Vikunja Server.
The goal is to support a command line based task workflow ~ similar to taskwarrior.

#### Breaking changes in vja 4.0
vja 4.0 supports (and requires) the most recent Vikunja API 0.24.0.
Use vja up to version 3.3.1 for compatibility with Vikunja API 0.23.0.

#### Breaking changes in vja 3.0
vja 3.0 supports (and requires) Vikunja API > 0.22.0.
Use vja up to version 2.4.1 for compatibility with Vikunja API 0.21.0.

## Usage

```shell
vja --help
vja ls
```

(You will be prompted for your account on first usage and any time the access token expires, see [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md#login))

**More user documentation is available on [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md)**


## Installation

- Install from pypi:
  ```shell
  python -m pip install --user vja
  vja --help
  ```
- Upgrade existing version:
  ```shell
  python -m pip install --user vja --upgrade
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
  Especially, the api_url must be reachable from your client. This can be verified, for example,
  by `curl https://mydomain.com/api/v1/info`.

You may change the location of the configuration directory with an environment variable
like `VJA_CONFIGDIR=/not/my/home`

### Description of configuration

#### Required options

| Section       | Option       | Description                                                 |
|---------------|--------------|-------------------------------------------------------------|
| [application] | api_url      | The service instance of Vikunja to which vja should connect |
| [application] | frontend_url | Required to open Vikunja in Browser                         |

#### Optional options

| Section                | Option              | Description                                                                                                                                                                                                                                                                                                  |
|------------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [output]               | arbitrary_name      | Python format strings which may be referenced on the command line by `--custom-format=<option_name>`. May contain any valid python f-Format string.<br>Take care: The format string may provide code which will be executed at runtime! Do not use `--custom-format` if you are unsure.<br> Default: missing |
| [output]               | another_format      | Multiple formats can be defined for reference. (see above)                                                                                                                                                                                                                                                   |
| [urgency_coefficients] | due_date_weight     | Weight of dueness in urgency score. Default: 1.0                                                                                                                                                                                                                                                             |
| [urgency_coefficients] | priority_weight     | Weight of priority in urgency score. Default: 1.0                                                                                                                                                                                                                                                            |
| [urgency_coefficients] | favorite_weight     | Weight of is_favorite in urgency score. Default: 1.0                                                                                                                                                                                                                                                         |
| [urgency_coefficients] | project_weight      | Weight of keyword occurrence in project title in urgency score. Default: 1.0                                                                                                                                                                                                                                 |
| [urgency_coefficients] | label_weight        | Weight of keyword occurrence in label title in urgency score. Default: 1.0                                                                                                                                                                                                                                   |
| [urgency_keywords]     | lisproject_keywords | Tasks in projects with a title containing these keywords are considered more urgent. Default: None                                                                                                                                                                                                           |
| [urgency_keywords]     | label_keywords      | Tasks labeled with one of these keywords are considered more urgent. Default: None                                                                                                                                                                                                                           |

## Development

### Prepare python virtual environment

Python >= 3.8 is recommended. First create a local environment:

```shell
python -m venv ./venv
source venv/bin/activate
```
(That may be `source venv/Scripts/activate` on some windows machines.)

### Local build

#### Local development install

```shell
python -m pip install -r requirements_dev.txt
python -m pip install -e .
```

#### Run integration test
Start docker container for `vikunja/api:latest` and execute `pytest` against that server instance.

```shell
docker compose -f tests/docker-compose.yml up -d
VJA_CONFIGDIR=tests/.vjatest pytest
docker compose -f tests/docker-compose.yml down
```

