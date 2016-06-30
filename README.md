draftjs_exporter [![Build Status](https://travis-ci.org/springload/draftjs_exporter.svg?branch=master)](https://travis-ci.org/springload/draftjs_exporter) [![Code Climate](https://codeclimate.com/github/springload/draftjs_exporter/badges/gpa.svg)](https://codeclimate.com/github/springload/draftjs_exporter)
================

> Python port of the [draftjs_exporter](https://github.com/ignitionworks/draftjs_exporter) ruby library.

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
make help            # See what commands are available.
make init            # Install dependencies and initialise for development.
make lint            # Lint the project.
make test            # Test the project.
make test-watch      # Restarts the tests whenever a file changes.
make test-ci         # Check for continuous integration.
make dev             # Restarts the example whenever a file changes.
make clean-pyc       # Remove Python file artifacts.
```

### Debugging

- Always run the tests. `npm install -g nodemon`, then `make test_watch`.
- Use a debugger. `pip install ipdb`, then `import ipdb; ipdb.set_trace()`.

## R&D notes

### Useful resources

#### Draft.js

- https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2
- https://github.com/nikgraf/awesome-draft-js
- https://github.com/rajaraodv/draftjs-examples
- https://github.com/lokiuz/redraft

### Generating HTML in Python

> https://www.quora.com/What-is-an-easy-to-use-HTML-XML-parser-generator-library-in-Python-similar-to-Hpricot-Nokogiri-in-Ruby

- http://lxml.de/
- https://www.crummy.com/software/BeautifulSoup/
- https://github.com/html5lib/html5lib-python
- http://www.yattag.org/
- http://markup.sourceforge.net/

### Limitations of `lxml`

- Succinct documentation (http://lxml.de/tutorial.html is the best)
- XML parser first, not really meant to generate HTML
- No support for document fragments
- No support for text nodes (`.text` and `.tail` instead)

### Under consideration

- Use https://github.com/icelab/draft-js-ast-exporter for its less ambiguous but also more opinionated exchange format?
- Use https://github.com/html5lib/html5lib-python for its nicer API, but the documentation is even worse than lxml.

### Other approaches

> Create the HTML in JS when you save it in draft, then apply a similar strategy to Wagtail’s Rich Text, by iterating over the output with regexes?
> Still get the benefits of a _much_ improved quality of editor. That way we can code awesome FP goodness.

- `contentState` to JSON, Python doing JSON to HTML, with this contentState -> HTML exporter
- `contentState` to AST to JSON, with AST to HTML in Python
- `contentState` to AST to HTML, with extra Python regexes
- `contentState` to HTML, with extra Python regexes

and it's not just contentState but contentState + some config

#### Constraints (to be weighted)

- Keeping the coupling between the CMS and the editor low so that we can change the editor's capabilities without having to write back-end code
- Giving the CMS enough control over the generated HTML. Not sure if "the CMS" just means "back-end" or if some JS code next to the editor code counts as well.
- Maintaining this over time with changing Draft.js output formats and unmaintained or wildly changing AST formats
- Regardless of implementation, being on the right spot between: "over the lifetime of the site/CMS, a given piece of content should always render the same HTML" and "a piece of content should always render the _best_ HTML"
- Keeping the coupling between CMS and editor low so that we can swap editors easily (bigger scope than the one of a single site/project here)
- Favour logical completeness over raw speed. The Wagtail regex parser will be faster than building a DOM. But caching makes that mostly irrelevant. The bottlenecks will all likely be in the DB lookups for inline entities anyway.
