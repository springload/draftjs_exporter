.. image:: https://travis-ci.org/springload/draftjs_exporter.svg?branch=master
   :target: https://travis-ci.org/springload/draftjs_exporter
.. image:: https://img.shields.io/pypi/v/draftjs_exporter.svg
   :target: https://pypi.python.org/pypi/draftjs_exporter
.. image:: https://coveralls.io/repos/github/springload/draftjs_exporter/badge.svg?branch=master
   :target: https://coveralls.io/github/springload/draftjs_exporter?branch=master
.. image:: https://codeclimate.com/github/springload/draftjs_exporter/badges/gpa.svg
   :target: https://codeclimate.com/github/springload/draftjs_exporter

draftjs_exporter 🐍
===================

    Library to convert the Facebook Draft.js editor’s raw ContentState to HTML.

This is a work in progress. It is intended to be integrated into `Wagtail CMS`_.

Usage
-----

Understanding DraftJS contentState
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unlike traditional rich text editors, DraftJS stores data in a JSON representation.

There are two main parts:

-  blocks - lines of data amd inline style attributes (without
   newlines).
-  entityMap – collection of `Entities`_

For more information, `this article`_ covers the concepts in depth.

Using the exporter
~~~~~~~~~~~~~~~~~~

.. code:: sh

    pip install draftjs_exporter

The library requires you to explicity define mappings for the types of blocks and entities you wish to render. We may provide some defaults in the future.

.. code:: python

    from draftjs_exporter.entities.link import Link
    from draftjs_exporter.html import HTML

    # Configure your element mappings and entity decorators
    config = {
        'entity_decorators': {
            'LINK': Link()
        },
        'block_map': {
            'header-two': {'element': 'h2'},
            'blockquote': {'element': 'blockquote'},
            'unstyled': {'element': 'p'}
        },
        'style_map': {
            'ITALIC': {'fontStyle': 'italic'},
            'BOLD': {'fontStyle': 'bold'}
        }
    }

    # Initialise the exporter with your configuration
    exporter = HTML(config)

    # Supply a draftJS `contentState`
    content_state = {
        'entityMap': {},
        'blocks': [
            {
                'key': '6mgfh',
                'text': 'User experience (UX) design',
                'type': 'header-two',
                'depth': 0,
                'inlineStyleRanges': [
                    {
                        'offset': 16,
                        'length': 4,
                        'style': 'BOLD'
                    }
                ],
                'entityRanges': []
            }
        ]
    }

    # Render markup
    markup = exporter.render(content_state)

Running the example
~~~~~~~~~~~~~~~~~~~

You can run an executable example as follows:

.. code:: sh

    python example.py

Feature list
~~~~~~~~~~~~

This project adheres to `Semantic Versioning`_ and `measures code coverage`_.

*  Extensive configuration of the generated HTML.
*  Default, extensible block & inline style maps for common HTML elements.
*  Define any attribute in the block map – custom class names for elements.
*  React-like API to create custom entity decorators.
*  Automatic conversion of entity data to HTML attributes (int & boolean to string, ``className`` to ``class``).
*  Wrapped blocks (``<li>`` elements go inside ``<ul>``).
*  Nested wrapped blocks (multiple list levels, arbitrary type and depth).
*  Output inline styles as inline elements (``<em>``, ``<strong>``, pick and choose).
*  Overlapping inline style ranges.

Development
-----------

Installation
~~~~~~~~~~~~

    Requirements: ``virtualenv``, ``pyenv``, ``twine``

.. code:: sh

    git clone git@github.com:springload/draftjs_exporter.git
    cd draftjs_exporter/
    virtualenv .venv
    source ./.venv/bin/activate
    make init
    # Optionally, install the git hooks
    ./.githooks/deploy
    # Optionally, install all tested python versions
    pyenv install 2.7.11 && pyenv install 3.3.6 && pyenv install 3.4.4 && pyenv install 3.5.1
    pyenv global system 2.7.11 3.3.6 3.4.4 3.5.1

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

*  Update the `changelog`_.
*  Update the version number in ``draftjs_exporter/__init__.py``, following semver.
*  ``git release vx.y.z``
*  ``make publish`` (confirm, and enter your password)
*  Go to https://pypi.python.org/pypi/draftjs_exporter and check that
   all is well

Documentation
-------------

    See the `docs/`_ folder

.. _Wagtail CMS: https://wagtail.io
.. _Entities: https://facebook.github.io/draft-js/docs/advanced-topics-entities.html#content
.. _this article: https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2
.. _Semantic Versioning: http://semver.org/spec/v2.0.0.html
.. _measures code coverage: https://coveralls.io/github/springload/draftjs_exporter?branch=master
.. _changelog: https://github.com/springload/draftjs_exporter/CHANGELOG.md
.. _docs/: https://github.com/springload/draftjs_exporter/docs/
