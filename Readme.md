# CLI client for Vikunja

[![pypi package version](https://img.shields.io/pypi/v/vja)](https://pypi.org/project/vja/)
[![pypi downloads](https://img.shields.io/pypi/dw/vja)](https://pypi.org/project/vja/)
[![pipeline status](https://gitlab.com/ce72/vja/badges/main/pipeline.svg)](https://gitlab.com/ce72/vja/-/pipelines)
[![coverage report](https://gitlab.com/ce72/vja/badges/main/coverage.svg)](https://gitlab.com/ce72/vja/commits/main)

This is a simple CLI for Vikunja > [The todo app to organize your life.](https://vikunja.io/)

It provides a command line interface for adding, viewing and editing todo tasks on a Vikunja Server.
The goal is to support a command line based task workflow ~ similar to taskwarrior.

> #### Breaking changes in vja 2.0
> vja 2.0 supports (and requires) the most recent Vikunja API > 0.20.4.
> In the wake of this transition the following breaking modifications to the vja command line interface have been
> introduced:
> - Labels: Are now given with `-l` (`-label`). (`-t` and `--tag` are no longer supported).
> - "Namespaces": Vikunja removed namespaces in favor of nested projects. `-n` (`--namespace`) was removed as option
    from `vja ls`.
> - Projects (former "lists"): Must be given with `-o` (`--project`). `vja ls -u` may be used to filter on the project
    or an upper project. This more or less resembles the old namespaces.
>
> Examples and more details can be found in the
> updated [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md)

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

## Usage

```shell
vja --help
vja ls
```

(You will be prompted for your account on first usage and any time the access token expires.)

**More documentation is available on [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md)**

## Development

### Prepare python virtual environment

Python >= 3.8 is recommended. First create a local environment:

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Local build

Build, install and perform some integration-test. For integration test, a real Vikunja instance is launched locally via
docker-compose.
Local development install:

```shell
pip install -r requirements_dev.txt
pip install -e .
```

Alternatively: full local installation:

```shell
# pip uninstall -y vja;rm -rf build dist vja.egg-info; python setup.py sdist bdist_wheel; pip install dist/*.whl;
```

Run integration test (requires docker and docker-compose)

```shell
docker-compose -f tests/docker-compose.yml up -d
VJA_CONFIGDIR=tests/.vjatest pytest
docker-compose -f tests/docker-compose.yml down
```

