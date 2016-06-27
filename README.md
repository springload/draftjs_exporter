# Draft Exporter [![Build Status](https://travis-ci.org/springload/draftjs_exporter.svg?branch=master)](https://travis-ci.org/springload/draftjs_exporter)

Python port of [draftjs_exporter](https://github.com/ignitionworks/draftjs_exporter) ruby library

This is a work in progress.

## Usage
```
python ./example.py
```

## Development

```sh
git clone git@github.com:springload/draftjs_exporter.git
cd draftjs_exporter/
virtualenv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## R&D notes

### Generating HTML in Python

> https://www.quora.com/What-is-an-easy-to-use-HTML-XML-parser-generator-library-in-Python-similar-to-Hpricot-Nokogiri-in-Ruby

- http://lxml.de/
- https://www.crummy.com/software/BeautifulSoup/
- https://github.com/html5lib/html5lib-python
- http://www.yattag.org/
- http://markup.sourceforge.net/
