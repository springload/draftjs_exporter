# Draft Exporter [![Build Status](https://travis-ci.org/springload/draftjs_exporter.svg?branch=master)](https://travis-ci.org/springload/draftjs_exporter)

Python port of [draftjs_exporter](https://github.com/ignitionworks/draftjs_exporter) ruby library

This is a work in progress.

## Usage
```
python ./example.py
```

## Development

### Installation

> Requirements: `virtualenv`, (`nodemon`)

```sh
git clone git@github.com:springload/draftjs_exporter.git
cd draftjs_exporter/
virtualenv .venv
source ./.venv/bin/activate
make init
./.githooks/deploy
```

### Commands

```sh
make dev             # Restarts the example whenever a file changes.
make help            # See what commands are available.
make init            # Install dependencies and initialise for development.
make lint            # Lint the project.
make test            # Test the project.
make test_watch      # Restarts the tests whenever a file changes.
```

## R&D notes

### Generating HTML in Python

> https://www.quora.com/What-is-an-easy-to-use-HTML-XML-parser-generator-library-in-Python-similar-to-Hpricot-Nokogiri-in-Ruby

- http://lxml.de/
- https://www.crummy.com/software/BeautifulSoup/
- https://github.com/html5lib/html5lib-python
- http://www.yattag.org/
- http://markup.sourceforge.net/

### Limitations of `lxml`

- Succinct documentation
- No support for document fragments
- No support for text nodes (`.text` and `.tail` instead)

Feels like we would want to use https://github.com/html5lib/html5lib-python but the documentation is even worse.
