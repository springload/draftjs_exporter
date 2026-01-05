# Repository Guidelines

## Project structure & module organization

Source code lives in `draftjs_exporter/`. Tests are in `tests/`. Contributor and user docs are in `docs/`. Type-checking stubs live in `stubs/`. The root also contains `example.py` and `benchmark.py` for local runs and performance checks.

## Development commands

- `make help`: See what commands are available.
- `make init`: Install dependencies and initialise for development.
- `make lint`: Lint the project.
- `make format`: Format project files.
- `make test`: Test the project.
- `make test-watch`: Restarts the tests whenever a file changes.
- `make test-coverage`: Run the tests while generating test coverage data.
- `make test-compatibility`: Compatibility-focused test suite.
- `make dev`: Restarts the example whenever a file changes.
- `make benchmark`: Runs a one-off performance (speed, memory) benchmark.
- `make clean-pyc`: Remove Python file artifacts.
- `make build`: Builds package for publication.
- `make publish`: Publishes a new version to PyPI.

## Project tools

- `uv` for dependency management
- `ruff` for linting and formatting
- `mypy` for type checking
- `ty` for additional type checking (experimental)
- `uv` for package publication
- `GitHub Actions` for continuous integration
- `pytest` for unit tests

## Coding style & naming conventions

- Python uses 4-space indentation and type annotations checked with mypy / ty.
- Formatting is enforced by `ruff format` for Python and `prettier` for all other files.
- Test modules follow `test_*.py`, with test functions named `test_*`.

## Testing guidelines

- Target of 100% test coverage for all improvements.
- Write tests both at the unit level but also integration (`test_exports.py`, `test_output.py`)
- Write implementation and language-agnostic test cases in `test_exports.json`

## Commit & pull request guidelines

- Be concise and to the point. Explain rationales that aren’t obvious.
- No Title Case usage ever. Always use Sentence case.
- Recent commit messages use short, capitalized, imperative summaries (e.g., “Enforce additional mypy check”).
- PRs should include a clear description, relevant test evidence (command + result), links to any related issues.
