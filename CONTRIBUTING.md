# Contributing to vja

`vja` is a CLI client (and MCP server) for the [Vikunja](https://vikunja.io/)
todo API. Contributions of any kind are welcome.

- Report issues: https://gitlab.com/ce72/vja/-/issues
- Submit merge requests: https://gitlab.com/ce72/vja/-/merge_requests

## Development setup

Create and activate a virtual environment, then install the package in editable
mode together with the development dependencies:

```shell
python -m venv ./venv
source venv/bin/activate          # venv/Scripts/activate on Windows
python -m pip install -r requirements_dev.txt
python -m pip install -e ".[mcp]"
```

`.[mcp]` also pulls in the optional `mcp` dependency needed for the MCP server.

## Commit messages

Releases are automated with
[semantic-release](https://semantic-release.gitbook.io/) and the version bump is
derived from the commit history, so commits **must** follow the
[Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<optional scope>): <description>
```

The type controls the release that a merge to `main` produces:

| Type                          | Release | Changelog section |
|-------------------------------|---------|-------------------|
| `feat`                        | minor   | Features          |
| `fix`                         | patch   | Bug Fixes         |
| `perf`, `refactor`            | patch   | Misc              |
| `docs` (`doc`)                | patch   | Documentation     |
| `ci`, `test` (`tests`)        | patch   | Automation        |
| `chore`                       | none    | Misc              |
| any type with `!` / `BREAKING CHANGE:` footer | major | — |

Use the `no-release` scope (e.g. `chore(no-release): ...`) to explicitly skip a
release. See [.releaserc.yml](.releaserc.yml) for the full configuration.

