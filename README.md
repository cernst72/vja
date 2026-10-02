[![pypi package version](https://img.shields.io/pypi/v/vja)](https://pypi.org/project/vja/)
[![pypi downloads](https://img.shields.io/pypi/dw/vja)](https://pypi.org/project/vja/)
[![pipeline status](https://gitlab.com/ce72/vja/badges/main/pipeline.svg)](https://gitlab.com/ce72/vja/-/pipelines)
[![coverage report](https://gitlab.com/ce72/vja/badges/main/coverage.svg)](https://gitlab.com/ce72/vja/commits/main)

# vja

A command line interface for [Vikunja](https://vikunja.io/), the open-source todo app to organize your life.

`vja` lets you add, view and edit your Vikunja tasks and projects directly from the terminal. The goal
is a fast, command line based task workflow, similar in spirit to taskwarrior. It also ships an
[MCP server](#mcp-server) so AI agents can manage your tasks.

```shell
vja add "Buy milk" --due=tomorrow --priority=3   # add a task
vja ls                                           # list active tasks, sorted by urgency
vja check 1                                       # mark task 1 as done
```

Highlights:

- Add, list, edit, defer, clone and delete tasks, with natural-language dates and reminders
- Powerful filtering and sorting, plus an urgency score you can tune
- Manage projects, labels and kanban buckets
- Custom output formats for scripting
- Optional MCP server to drive vja from AI agents

**More user documentation is in [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md).**

> **❗ Important change in vja 6.0.0** — a Vikunja server with version >= 2.5.0 is required, and
> `api_url` must point to `/v2`, e.g. `api_url=https://my.domain/api/v2`.

## Table of contents
<!-- TOC -->
* [vja](#vja)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
    * [Install with pipx (recommended)](#install-with-pipx-recommended)
    * [Install with pip](#install-with-pip)
  * [Configuration](#configuration)
    * [Description of configuration](#description-of-configuration)
      * [Required options](#required-options)
      * [Optional options](#optional-options)
  * [Usage](#usage)
  * [Shell completion](#shell-completion)
    * [Bash](#bash)
    * [Zsh](#zsh)
    * [Fish](#fish)
  * [MCP server](#mcp-server)
  * [Development](#development)
    * [Prepare python virtual environment](#prepare-python-virtual-environment)
    * [Local build](#local-build)
      * [Local development install](#local-development-install)
      * [Run integration test](#run-integration-test)
<!-- TOC -->

## Installation

### Install with pipx (recommended)

(More on pipx [here](https://pipx.pypa.io/stable/).)

```shell
pipx install vja
```

To install vja with MCP support from the start, install the optional extra instead:

```shell
pipx install "vja[mcp]"
```

To add MCP support to an existing pipx installation of vja, install its dependency into that
environment:

```shell
pipx inject vja "mcp>=2"
```

Upgrade an existing version:

```shell
pipx upgrade vja
```

This upgrades vja and its dependencies as needed. If MCP support was added with `pipx inject`,
upgrade the injected MCP dependency as well:

```shell
pipx upgrade vja --include-injected
```

To explicitly upgrade the MCP package even when its installed version already satisfies the
`mcp>=2` requirement, run:

```shell
pipx runpip vja install --upgrade mcp
```

### Install with pip

Not recommended because it does not isolate vja's dependencies from other Python packages.

```shell
python -m pip install --user vja
vja --help
```

## Configuration

Before using `vja` you must provide a configuration.
`vja` looks for its configuration at the following paths (in order):

1. `$VJA_CONFIGDIR/config.rc`
2. `$XDG_CONFIG_HOME/vja/config.rc`
3. `$HOME/.config/vja/config.rc`
4. `$HOME/.vjacli/vja.rc` (deprecated - for backward compatibility only)

A full example can be found in [config.rc](https://gitlab.com/ce72/vja/-/blob/main/.config/vja/config.rc).

- Create a configuration file at any valid path (see above) with the following minimal contents:
  ```ini
  [application]
  frontend_url=https://try.vikunja.io/
  api_url=https://try.vikunja.io/api/v2
  ```
  (If you cloned from git, you may copy the folder `.config/vja` to your `$HOME/.config` directory instead.)
- Adjust to your needs. `frontend_url` and `api_url` must point to your own Vikunja server.
  In particular, `api_url` must be reachable from your client. You can verify this, for example,
  with `curl https://mydomain.com/api/v2/info`.

You may change the location of the configuration directory with an environment variable
like `VJA_CONFIGDIR=/not/my/home`.

### Description of configuration

#### Required options

| Section         | Option         | Description                                                 |
|-----------------|----------------|-------------------------------------------------------------|
| `[application]` | `api_url`      | The Vikunja instance vja should connect to                  |
| `[application]` | `frontend_url` | Base URL used to open Vikunja in the browser                |

#### Optional options

| Section                  | Option             | Description                                                                                   |
|--------------------------|--------------------|-----------------------------------------------------------------------------------------------|
| `[output]`               | *(custom formats)* | Named python format strings for `--custom-format`. See [Output format](https://gitlab.com/ce72/vja/-/blob/main/Features.md#output-format). |
| `[urgency_coefficients]` | `due_date_weight`  | Weight of dueness in the urgency score. Default: 1.0                                           |
| `[urgency_coefficients]` | `priority_weight`  | Weight of priority in the urgency score. Default: 1.0                                          |
| `[urgency_coefficients]` | `favorite_weight`  | Weight of is_favorite in the urgency score. Default: 1.0                                       |
| `[urgency_coefficients]` | `project_weight`   | Weight of keyword occurrence in the project title (see `project_keywords`). Default: 1.0       |
| `[urgency_coefficients]` | `label_weight`     | Weight of keyword occurrence in label titles (see `label_keywords`). Default: 1.0              |
| `[urgency_keywords]`     | `project_keywords` | Tasks in projects whose title contains one of these keywords are more urgent. Default: None    |
| `[urgency_keywords]`     | `label_keywords`   | Tasks labeled with one of these keywords are more urgent. Default: None                        |

## Usage

Once installed and configured, run:

```shell
vja --help
vja ls
```

On first usage (and whenever the access token expires) you will be prompted for your account. See
[Login in Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md#login) for details and the
API-token alternative, and [Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md) for the
full command reference.

## Shell completion

Shell tab-completion can be enabled by generating a shell completion script (not specific to vja):

### Bash
```sh
mkdir -p ~/.config/bash/completions
_VJA_COMPLETE=bash_source vja > ~/.config/bash/completions/vja
```
Then add to your `~/.bashrc`:
```sh
source ~/.config/bash/completions/vja
```
Note: Instead of sourcing the completion script in `.bashrc` you can just move it to a folder which is supported by bash_completion (e.g. `~/.local/share/bash-completion/completions/`).

### Zsh
```sh
mkdir -p ~/.config/zsh/completions
_VJA_COMPLETE=zsh_source vja > ~/.config/zsh/completions/vja.zsh
```
Then add to your `~/.zshrc`:
```sh
source ~/.config/zsh/completions/vja.zsh
```
Note: The script location is just a suggestion; you can put it wherever you like.
If you use [ohmyzsh](https://ohmyz.sh), place completion scripts under
`~/.oh-my-zsh/custom/completions`.

### Fish
```sh
_VJA_COMPLETE=fish_source vja > ~/.config/fish/completions/vja.fish
```
Note: Fish completions in the directory above will be automatically loaded for new sessions.

## MCP server

Besides the CLI, `vja` can act as an [MCP](https://modelcontextprotocol.io) server so AI agents
(Claude, Kiro, Cursor, ...) can manage your Vikunja tasks. Install the optional dependency and
register the `vja-mcp` command with your client:

```shell
pipx install "vja[mcp]"   # or: python -m pip install --user "vja[mcp]"
```
For client configuration, available tools, and other MCP details, see the
[MCP server documentation in Features.md](Features.md#mcp-server-use-vja-from-ai-agents).

```json
{
  "mcpServers": {
    "vja": {
      "command": "vja-mcp"
    }
  }
}
```

The server uses the same configuration as the CLI. See
[Features.md](https://gitlab.com/ce72/vja/-/blob/main/Features.md#mcp-server-use-vja-from-ai-agents)
for the available tools and [AGENTS.md](https://gitlab.com/ce72/vja/-/blob/main/AGENTS.md) for
agent-specific guidance.

## Development

### Prepare python virtual environment

First create a local environment:

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

Start docker container for `vikunja/api:latest` and execute `pytest` against that server instance:

```shell
docker compose -f tests/docker-compose.yml up -d
VJA_CONFIGDIR=tests/.vjatest pytest
docker compose -f tests/docker-compose.yml down
```
