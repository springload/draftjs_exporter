# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

Please note that this project is released with a [Contributor Code of Conduct](docs/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

[![Code Climate for draftjs_exporter](https://codeclimate.com/github/springload/draftjs_exporter/badges/gpa.svg)](https://codeclimate.com/github/springload/draftjs_exporter)

## Development

### Installation

> Requirements: `virtualenv`, `pyenv`

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
pyenv install --skip-existing 2.7.11
pyenv install --skip-existing 3.4.4
pyenv install --skip-existing 3.5.1
pyenv install --skip-existing 3.6.3
# Make required Python versions available globally.
pyenv global system 2.7.11 3.4.4 3.5.1 3.6.3
```

### Commands

```sh
make help            # See what commands are available.
make init            # Install dependencies and initialise for development.
make lint            # Lint the project.
make test            # Test the project.
make test-watch      # Restarts the tests whenever a file changes.
make test-coverage   # Run the tests while generating test coverage data.
make test-ci         # Continuous integration test suite.
make dev             # Restarts the example whenever a file changes.
make benchmark       # Runs a one-off performance (speed, memory) benchmark.
make clean-pyc       # Remove Python file artifacts.
make publish         # Publishes a new version to pypi.
```

### Debugging

* Always run the tests. `npm install -g nodemon`, then `make test-watch`.
* Use a debugger. `pip install ipdb`, then `import ipdb; ipdb.set_trace()`.

### Releases

* Make a new branch for the release of the new version.
* Update the [CHANGELOG](https://github.com/springload/draftjs_exporter/CHANGELOG.md).
* Update the version number in `draftjs_exporter/__init__.py`, following semver.
* Make a PR and squash merge it.
* Back on master with the PR merged, use `make publish` (confirm, and enter your password).
* Finally, go to GitHub and create a release and a tag for the new version.
* Done!

> As a last step, you may want to go update our [Draft.js exporter demo](https://github.com/springload/draftjs_exporter_demo) to this new release to check that all is well in a fully separate project.

## Documentation

> See the [docs](https://github.com/springload/draftjs_exporter/tree/master/docs) folder.
