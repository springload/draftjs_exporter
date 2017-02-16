.. image:: https://img.shields.io/pypi/v/draftjs_exporter.svg
   :target: https://pypi.python.org/pypi/draftjs_exporter
.. image:: https://travis-ci.org/springload/draftjs_exporter.svg?branch=master
   :target: https://travis-ci.org/springload/draftjs_exporter
.. image:: https://coveralls.io/repos/github/springload/draftjs_exporter/badge.svg?branch=master
   :target: https://coveralls.io/github/springload/draftjs_exporter?branch=master
.. image:: https://codeclimate.com/github/springload/draftjs_exporter/badges/gpa.svg
   :target: https://codeclimate.com/github/springload/draftjs_exporter

draftjs_exporter 🐍
===================

    Library to convert the Facebook Draft.js editor’s raw ContentState to HTML.

It is developed alongside the `Draftail <https://github.com/springload/draftail/>`_ rich text editor, for integration into `Wagtail <https://wagtail.io/>`_. Check out `wagtaildraftail <https://github.com/springload/wagtaildraftail>`_ and the `online demo <https://draftjs-exporter.herokuapp.com/>`_!

Features
--------

This project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_, and measures performance and `code coverage <https://coveralls.io/github/springload/draftjs_exporter>`_.

*  Extensive configuration of the generated HTML.
*  Default, extensible block & inline style maps for common HTML elements.
*  Convert line breaks to ``<br>`` elements.
*  Define any attribute in the block map – custom class names for elements.
*  React-like API to create custom components.
*  Automatic conversion of entity data to HTML attributes (int & boolean to string, ``className`` to ``class``).
*  Wrapped blocks (``<li>`` elements go inside ``<ul>`` or ``<ol>``).
*  Nested wrapped blocks (multiple nesting levels, arbitrary type and depth).
*  Output inline styles as inline elements (``<em>``, ``<strong>``, pick and choose).
*  Overlapping inline style ranges.

Usage
-----

Draft.js stores data in a JSON representation based on blocks, representing lines of content in the editor, annotated with entities and styles to represent rich text. For more information, `this article <https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2>`_ covers the concepts further.

Getting started
~~~~~~~~~~~~~~~

This exporter takes the Draft.js ContentState data as input, and outputs HTML based on its configuration. To get started, install the package:

.. code:: sh

    pip install draftjs_exporter

In your code, create an exporter and use the ``render`` method to create HTML:

.. code:: python

    from draftjs_exporter.html import HTML

    # Configuration options are detailed below.
    config = {}

    # Initialise the exporter.
    exporter = HTML(config)

    # Render a Draft.js `contentState`
    html = exporter.render({
        'entityMap': {},
        'blocks': [{
            'key': '6mgfh',
            'text': 'Hello, world!',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }]
    })


You can also run an example by downloading this repository and then using ``python example.py``.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

The exporter output is extensively configurable to cater for varying content types.

.. code:: python

    # draftjs_exporter provides default configurations and predefined constants for reuse.
    from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
    from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP

    # The configuration is a single object with predefined keys.
    config = {
        # `block_map` is a mapping from Draft.js block types to a definition of their HTML representation.
        # Extend BLOCK_MAP to start with sane defaults, or make your own from scratch.
        'block_map': dict(BLOCK_MAP, **{
            # The most basic mapping format, block type to tag name.
            BLOCK_TYPES.HEADER_TWO: {'element': 'h2'},
            # TODO Describe full configuration below.
            BLOCK_TYPES.BLOCKQUOTE: ['blockquote', {'className': 'c-pullquote'}],
            BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                'element': 'li',
                'wrapper': ['ul', {'className': 'bullet-list'}],
            },
        }),
        # Extend/override the default style map.
        'style_map': dict(STYLE_MAP, **{
            'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
        }),
        'entity_decorators': {
            ENTITY_TYPES.LINK: Link(use_new_window=True),
            ENTITY_TYPES.IMAGE: Image,
            ENTITY_TYPES.HORIZONTAL_RULE: HR,
        },
        'composite_decorators': [
            BR,
            Hashtag,
        ],
    }

See ``examples.py`` for more details.

Development
-----------

Installation
~~~~~~~~~~~~

    Requirements: ``virtualenv``, ``pyenv``, ``twine``

.. code:: sh

    git clone git@github.com:springload/draftjs_exporter.git
    cd draftjs_exporter/
    # Install the git hooks.
    ./.githooks/deploy
    # Install the Python environment.
    virtualenv .venv
    source ./.venv/bin/activate
    make init
    # Install all tested python versions.
    pyenv install 2.7.11 && pyenv install 3.4.4 && pyenv install 3.5.1
    pyenv global system 2.7.11 3.4.4 3.5.1

Commands
~~~~~~~~

.. code:: sh

    make help            # See what commands are available.
    make init            # Install dependencies and initialise for development.
    make lint            # Lint the project.
    make test            # Test the project.
    make test-watch      # Restarts the tests whenever a file changes.
    make test-coverage   # Run the tests while generating test coverage data.
    make test-ci         # Continuous integration test suite.
    make dev             # Restarts the example whenever a file changes.
    make clean-pyc       # Remove Python file artifacts.
    make publish         # Publishes a new version to pypi.

Debugging
~~~~~~~~~

*  Always run the tests. ``npm install -g nodemon``, then ``make test-watch``.
*  Use a debugger. ``pip install ipdb``, then ``import ipdb; ipdb.set_trace()``.

Releases
~~~~~~~~

*  Update the `changelog <https://github.com/springload/draftjs_exporter/CHANGELOG.md>`_.
*  Update the version number in ``draftjs_exporter/__init__.py``, following semver.
*  ``git release vx.y.z``
*  ``make publish`` (confirm, and enter your password)
*  Go to https://pypi.python.org/pypi/draftjs_exporter and check that all is well.

Documentation
-------------

    See the `docs <https://github.com/springload/draftjs_exporter/docs/>`_ folder
