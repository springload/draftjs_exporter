# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

Please note that this project is released with a [Contributor Code of Conduct](docs/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Development

### Installation

> Requirements: `virtualenv`, [`pyenv`](https://github.com/pyenv/pyenv), [`nvm`](https://github.com/nvm-sh/nvm)

```sh
git clone git@github.com:springload/draftjs_exporter.git
cd draftjs_exporter/
# Install the git hooks.
./.githooks/deploy
# Install the Python environment.
virtualenv .venv
source ./.venv/bin/activate
make init
# Install required Python versions
pyenv install --skip-existing 3.8.5
pyenv install --skip-existing 3.9.1
pyenv install --skip-existing 3.10.0
pyenv install --skip-existing 3.11.0
pyenv install --skip-existing 3.12.1
pyenv install --skip-existing 3.13.0a2
# Make required Python versions available globally.
pyenv global system 3.8.5 3.9.1 3.10.0 3.11.0 3.12.0 3.13.0a2
```

### Commands

```sh
make help            # See what commands are available.
make init            # Install dependencies and initialise for development.
make lint            # Lint the project.
make format          # Format project files.
make test            # Test the project.
make test-watch      # Restarts the tests whenever a file changes.
make test-coverage   # Run the tests while generating test coverage data.
make test-ci         # Continuous integration test suite.
make dev             # Restarts the example whenever a file changes.
make benchmark       # Runs a one-off performance (speed, memory) benchmark.
make clean-pyc       # Remove Python file artifacts.
make build           # Builds package for publication.
make publish         # Publishes a new version to pypi.
```

### Debugging

- Always run the tests. `npm install -g nodemon`, then `make test-watch`.
- Use a debugger. `pip install ipdb`, then `import ipdb; ipdb.set_trace()`.

### Releases

- Make a new branch for the release of the new version.
- Update the [CHANGELOG](https://github.com/springload/draftjs_exporter/CHANGELOG.md).
- Update the version number in `draftjs_exporter/__init__.py`, following semver.
- Make a PR and squash merge it.
- Back on main with the PR merged, use `make publish` (confirm, and enter your password).
- Finally, go to GitHub and create a release and a tag for the new version.
- Done!

> As a last step, you may want to go update the [Draftail Playground](http://playground.draftail.org/) to this new release to check that all is well in a fully separate project.

## Documentation

> See the [docs](https://github.com/springload/draftjs_exporter/tree/main/docs) folder.
