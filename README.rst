.. image:: https://img.shields.io/pypi/v/draftjs_exporter.svg
   :target: https://pypi.python.org/pypi/draftjs_exporter
.. image:: https://travis-ci.org/springload/draftjs_exporter.svg?branch=master
   :target: https://travis-ci.org/springload/draftjs_exporter
.. image:: https://coveralls.io/repos/github/springload/draftjs_exporter/badge.svg?branch=master
   :target: https://coveralls.io/github/springload/draftjs_exporter?branch=master

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
*  Automatic conversion of entity data to HTML attributes (int & boolean to string, style object to style string).
*  Nested lists (``<li>`` elements go inside ``<ul>`` or ``<ol>``, with multiple levels).
*  Output inline styles as inline elements (``<em>``, ``<strong>``, pick and choose, with any attribute).
*  Overlapping inline style and entity ranges.

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

    print(html)

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
            BLOCK_TYPES.HEADER_THREE: {'element': 'h3', 'props': {'class': 'u-text-center'}},
            # Add a wrapper (and wrapper_props) to wrap adjacent blocks.
            BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                'element': 'li',
                'wrapper': 'ul',
                'wrapper_props': {'class': 'bullet-list'},
            },
            # Use a custom component for more flexibility (reading block data or depth).
            BLOCK_TYPES.BLOCKQUOTE: Blockquote,
            BLOCK_TYPES.ORDERED_LIST_ITEM: {
                'element': ListItem,
                'wrapper': OrderedList,
            },
            # Provide a fallback component (advanced).
            BLOCK_TYPES.FALLBACK: BlockFallback
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
            # Discard those entities.
            ENTITY_TYPES.EMBED: None,
            # Provide a fallback component (advanced).
            ENTITY_TYPES.FALLBACK: EntityFallback,
        },
        'composite_decorators': [
            # Use composite decorators to replace text based on a regular expression.
            BR,
            Hashtag,
            Linkify,
        ],
    }

See ``examples.py`` in the repository for more details.

Advanced usage
--------------

Custom components
~~~~~~~~~~~~~~~~~

To produce arbitrary markup with dynamic data, draftjs_exporter comes with an API to create rendering components. This API mirrors React's `createElement <https://facebook.github.io/react/docs/top-level-api.html#react.createelement>`_ API (what JSX compiles to).

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

Apart from ``create_element``, a ``parse_html`` method is also available. Use it to interface with other HTML generators, like template engines.

See ``examples.py`` in the repository for more details.

Fallback components
~~~~~~~~~~~~~~~~~~~

When dealing with changes in the content schema, as part of ongoing development or migrations, some content can go stale.
To solve this, the exporter allows the definition of fallback components for blocks, styles, and entities.
This feature is only used for development at the moment, if you have a use case for this in production we would love to hear from you. Please get in touch!

Add the following to the exporter config,

.. code:: python

    config = {
        'block_map': dict(BLOCK_MAP, **{
            # Provide a fallback for block types.
            BLOCK_TYPES.FALLBACK: BlockFallback
        }),
    }

This fallback component can now control the exporter behavior when normal components are not found. Here is an example:

.. code:: python

    def BlockFallback(props):
        type_ = props['block']['type']

        if type_ == 'example-discard':
            logging.warn('Missing config for "%s". Discarding block, keeping content.' % type_)
            # Directly return the block's children to keep its content.
            return props['children']
        elif type_ == 'example-delete':
            logging.error('Missing config for "%s". Deleting block.' % type_)
            # Return None to not render anything, removing the whole block.
            return None
        else:
            logging.warn('Missing config for "%s". Using div instead.' % type_)
            # Provide a fallback.
            return DOM.create_element('div', {}, props['children'])

See ``examples.py`` in the repository for more details.

lxml backing engine
~~~~~~~~~~~~~~~~~~~

By default the exporter uses ``html5lib`` via BeautifulSoup to build DOM tree. ``lxml`` is also supported. lxml is more performant, but it requires ``libxml2`` and `libxslt`` to be available on your system.

.. code:: sh

    # Use the `lxml` extra to install the exporter and its lxml dependencies:
    pip install draftjs_exporter[lxml]

Add the following to the exporter config:

.. code:: python

    config = {
        # Specify which DOM backing engine to use.
        'engine': 'lxml',
    }

Custom backing engines
~~~~~~~~~~~~~~~~~~~~~~

The exporter supports using custom engines to generate its output via the ``DOM`` API.
This feature is only used for development at the moment, if you have a use case for this in production we would love to hear from you. Please get in touch!

Here is an example implementation:

.. code:: python

    from draftjs_exporter import DOMEngine

    class DOMListTree(DOMEngine):
        """
        Element tree using nested lists.
        """

        @staticmethod
        def create_tag(t, attr=None):
            return [t, attr, []]

        @staticmethod
        def append_child(elt, child):
            elt[2].append(child)

        @staticmethod
        def render(elt):
            return elt


    exporter = HTML({'engine': DOMListTree})

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

*  Make a new branch for the release of the new version.
*  Update the `CHANGELOG <https://github.com/springload/draftjs_exporter/CHANGELOG.md>`_.
*  Update the version number in ``draftjs_exporter/__init__.py``, following semver.
*  Make a PR and squash merge it.
*  Back on master with the PR merged, use ``make publish`` (confirm, and enter your password).
*  Finally, go to GitHub and create a release and a tag for the new version.
*  Done!

Documentation
-------------

    See the `docs <https://github.com/springload/draftjs_exporter/docs/>`_ folder.
