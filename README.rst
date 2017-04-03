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
*  Nested lists (``<li>`` elements go inside ``<ul>`` or ``<ol>``, with multiple levels).
*  Output inline styles as inline elements (``<em>``, ``<strong>``, pick and choose, with any attribute).
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

    from draftjs_exporter.dom import DOM
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

    print(DOM.pretty_print(html))


You can also run an example by downloading this repository and then using ``python example.py``, or by using our `online demo <https://draftjs-exporter.herokuapp.com/>`_.

Configuration
~~~~~~~~~~~~~

The exporter output is extensively configurable to cater for varied rich text requirements.

.. code:: python

    # draftjs_exporter provides default configurations and predefined constants for reuse.
    from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
    from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
    from draftjs_exporter.dom import DOM

    config = {
        # `block_map` is a mapping from Draft.js block types to a definition of their HTML representation.
        # Extend BLOCK_MAP to start with sane defaults, or make your own from scratch.
        'block_map': dict(BLOCK_MAP, **{
            # The most basic mapping format, block type to tag name.
            BLOCK_TYPES.HEADER_TWO: 'h2',
            # Use a dict to define props on the block.
            BLOCK_TYPES.HEADER_THREE: {'element': 'h3', 'props': {'className': 'u-text-center'}},
            # Add a wrapper (and wrapper_props) to wrap adjacent blocks.
            BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                'element': 'li',
                'wrapper': 'ul',
                'wrapper_props': {'className': 'bullet-list'},
            },
            # Use a component for more flexibility (reading block data or depth).
            BLOCK_TYPES.BLOCKQUOTE: Blockquote,
            BLOCK_TYPES.ORDERED_LIST_ITEM: {
                'element': ListItem,
                'wrapper': 'ol',
            },
        }),
        # `style_map` defines the HTML representation of inline elements.
        # Extend STYLE_MAP to start with sane defaults, or make your own from scratch.
        'style_map': dict(STYLE_MAP, **{
            # Use the same mapping format as in the `block_map`.
            'KBD': 'kbd',
            # The `style` prop can be defined as a dict, that will automatically be converted to a string.
            'HIGHLIGHT': {'element': 'strong', 'props': {'style': {'textDecoration': 'underline'}}},
        }),
        'entity_decorators': {
            # Map entities to components so they can be rendered with their data.
            ENTITY_TYPES.IMAGE: Image,
            # Components can be defined as classes to receive extra parameters.
            ENTITY_TYPES.LINK: Link(use_new_window=True),
            # Lambdas work too.
            ENTITY_TYPES.HORIZONTAL_RULE: lambda props: DOM.create_element('hr'),
            ENTITY_TYPES.EMBED: None,
        },
        'composite_decorators': [
            # Use composite decorators to replace text based on a regular expression.
            BR,
            Hashtag,
            Linkify,
        ],
    }

See ``examples.py`` for more details.

Custom components
~~~~~~~~~~~~~~~~~

To produce arbitrary markup with dynamic data, draftjs_exporter comes with an API to create rendering components. This API mirrors React's `createElement <https://facebook.github.io/react/docs/top-level-api.html#react.createelement>`_ API (what compiled JSX produces).

.. code:: python

    # All of the API is available from a single `DOM` namespace
    from draftjs_exporter.dom import DOM


    # Components are simple functions that take `props` as parameter and return DOM elements.
    def Image(props):
        # This component creates an image element, with the relevant attributes.
        return DOM.create_element('img', {
            'src': props.get('src'),
            'width': props.get('width'),
            'height': props.get('height'),
            'alt': props.get('alt'),
        })


    def Blockquote(props):
        # This component uses block data to render a blockquote.
        block_data = props['block']['data']

        # Here, we want to display the block's content so we pass the `children` prop as the last parameter.
        return DOM.create_element('blockquote', {
            'cite': block_data.get('cite')
        }, props['children'])


    class Button:
        def render(self, props):
            href = props.get('href', '#')
            icon = props.get('icon', None)
            text = props.get('text', '')

            # There can be as many `children` as required.
            # It is also possible to reuse other components and render them instead of HTML tags.
            return DOM.create_element(
                'a',
                {'class': 'icon-text' if icon else None, 'href': href},
                DOM.create_element(Icon, {'name': icon}) if icon else None,
                DOM.create_element('span', {'class': 'icon-text__text'}, text) if icon else text
            )

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
    # Install required Python versions
    pyenv install --skip-existing 2.7.11
	pyenv install --skip-existing 3.4.4
	pyenv install --skip-existing 3.5.1
    # Make required Python versions available globally.
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
*  Done!

Documentation
-------------

    See the `docs <https://github.com/springload/draftjs_exporter/docs/>`_ folder.
