# Draft.js exporter [![PyPI](https://img.shields.io/pypi/v/draftjs_exporter.svg)](https://pypi.org/project/draftjs_exporter/) [![Travis](https://travis-ci.org/springload/draftjs_exporter.svg?branch=master)](https://travis-ci.org/springload/draftjs_exporter) [![Coveralls](https://coveralls.io/repos/github/springload/draftjs_exporter/badge.svg?branch=master)](https://coveralls.io/github/springload/draftjs_exporter?branch=master)

> Library to convert rich text from Draft.js raw ContentState to HTML.

It is developed alongside the [Draftail](https://github.com/springload/draftail/) rich text editor, for [Wagtail](https://github.com/wagtail/wagtail). Check out the [online demo](https://draftail-playground.herokuapp.com/), and our [introductory blog post](https://wagtail.io/blog/rethinking-rich-text-pipelines-with-draft-js/)

## Why

[Draft.js](https://draftjs.org/) is a rich text editor framework for React. Its approach is different from most rich text editors because it does not store data as HTML, but rather in its own representation called ContentState. This exporter is useful when the ContentState to HTML conversion has to be done in a Python ecosystem.

The initial use case was to gain more control over the content managed by rich text editors in a Wagtail/Django site. If you want to read the full story, have a look at our blog post: [Rethinking rich text pipelines with Draft.js](https://wagtail.io/blog/rethinking-rich-text-pipelines-with-draft-js/).

## Features

This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html), and [measures performance](http://blog.thib.me/python-memory-profiling-for-the-draft-js-exporter/) and [code coverage](https://coveralls.io/github/springload/draftjs_exporter).

* Extensive configuration of the generated HTML.
* Default, extensible block & inline style maps for common HTML elements.
* Convert line breaks to `<br>` elements.
* Define any attribute in the block map – custom class names for elements.
* React-like API to create custom components.
* Automatic conversion of entity data to HTML attributes (int & boolean to string, style object to style string).
* Nested lists (`<li>` elements go inside `<ul>` or `<ol>`, with multiple levels).
* Output inline styles as inline elements (`<em>`, `<strong>`, pick and choose, with any attribute).
* Overlapping inline style and entity ranges.

## Usage

Draft.js stores data in a JSON representation based on blocks,
representing lines of content in the editor, annotated with entities and
styles to represent rich text. For more information, [this
article](https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2)
covers the concepts further.

### Getting started

This exporter takes the Draft.js ContentState data as input, and outputs HTML based on its configuration. To get started, install the package:

```sh
pip install draftjs_exporter
```

In your code, create an exporter and use the `render` method to create HTML:

```python
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
```

You can also run an example by downloading this repository and then using `python example.py`, or by using our [online demo](https://draftail-playground.herokuapp.com/).

### Configuration

The exporter output is extensively configurable to cater for varied rich text requirements.

```python
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
        BLOCK_TYPES.BLOCKQUOTE: blockquote,
        BLOCK_TYPES.ORDERED_LIST_ITEM: {
            'element': list_item,
            'wrapper': ordered_list,
        },
        # Provide a fallback component (advanced).
        BLOCK_TYPES.FALLBACK: block_fallback
    }),
    # `style_map` defines the HTML representation of inline elements.
    # Extend STYLE_MAP to start with sane defaults, or make your own from scratch.
    'style_map': dict(STYLE_MAP, **{
        # Use the same mapping format as in the `block_map`.
        'KBD': 'kbd',
        # The `style` prop can be defined as a dict, that will automatically be converted to a string.
        'HIGHLIGHT': {'element': 'strong', 'props': {'style': {'textDecoration': 'underline'}}},
        # Provide a fallback component (advanced).
        INLINE_STYLES.FALLBACK: style_fallback,
    }),
    'entity_decorators': {
        # Map entities to components so they can be rendered with their data.
        ENTITY_TYPES.IMAGE: image,
        ENTITY_TYPES.LINK: link
        # Lambdas work too.
        ENTITY_TYPES.HORIZONTAL_RULE: lambda props: DOM.create_element('hr'),
        # Discard those entities.
        ENTITY_TYPES.EMBED: None,
        # Provide a fallback component (advanced).
        ENTITY_TYPES.FALLBACK: entity_fallback,
    },
    'composite_decorators': [
        # Use composite decorators to replace text based on a regular expression.
        {
            'strategy': re.compile(r'\n'),
            'component': br,
        },
        {
            'strategy': re.compile(r'#\w+'),
            'component': hashtag,
        },
        {
            'strategy': LINKIFY_RE,
            'component': linkify,
        },
    ],
}
```

See [examples.py](https://github.com/springload/draftjs_exporter/blob/master/example.py) for more details.

## Advanced usage

### Custom components

To generate arbitrary markup with dynamic data, the exporter comes with an API to create rendering components. This API mirrors React's [createElement](https://facebook.github.io/react/docs/top-level-api.html#react.createelement) API (what JSX compiles to).

```python
# All of the API is available from a single `DOM` namespace
from draftjs_exporter.dom import DOM


# Components are simple functions that take `props` as parameter and return DOM elements.
def image(props):
    # This component creates an image element, with the relevant attributes.
    return DOM.create_element('img', {
        'src': props.get('src'),
        'width': props.get('width'),
        'height': props.get('height'),
        'alt': props.get('alt'),
    })


def blockquote(props):
    # This component uses block data to render a blockquote.
    block_data = props['block']['data']

    # Here, we want to display the block's content so we pass the `children` prop as the last parameter.
    return DOM.create_element('blockquote', {
        'cite': block_data.get('cite')
    }, props['children'])


def button(props):
    href = props.get('href', '#')
    icon_name = props.get('icon', None)
    text = props.get('text', '')

    return DOM.create_element('a', {
            'class': 'icon-text' if icon_name else None,
            'href': href,
        },
        # There can be as many `children` as required.
        # It is also possible to reuse other components and render them instead of HTML tags.
        DOM.create_element(icon, {'name': icon_name}) if icon_name else None,
        DOM.create_element('span', {'class': 'icon-text'}, text) if icon_name else text
    )
```

Apart from `create_element`, a `parse_html` method is also available. Use it to interface with other HTML generators, like template engines.

See `examples.py` in the repository for more details.

### Fallback components

When dealing with changes in the content schema, as part of ongoing development or migrations, some content can go stale.
To solve this, the exporter allows the definition of fallback components for blocks, styles, and entities.
This feature is only used for development at the moment, if you have a use case for this in production we would love to hear from you.
Please get in touch!

Add the following to the exporter config,

```python
config = {
    'block_map': dict(BLOCK_MAP, **{
        # Provide a fallback for block types.
        BLOCK_TYPES.FALLBACK: block_fallback
    }),
}
```

This fallback component can now control the exporter behavior when normal components are not found. Here is an example:

```python
def block_fallback(props):
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
```

See `examples.py` in the repository for more details.

### Alternative backing engines

By default, the exporter uses a dependency-free engine called `string` to build the DOM tree. There are two alternative backing engines: `html5lib` (via BeautifulSoup) and `lxml`.

The `string` engine is the fastest, and does not have any dependencies. Its only drawback is that the `parse_html` method does not escape/sanitise HTML like that of other engines.

* For `html5lib`, do `pip install draftjs_exporter[html5lib]`.
* For `lxml`, do `pip install draftjs_exporter[lxml]`. It also requires `libxml2` and `libxslt` to be available on your system.

Then, use the `engine` attribute of the exporter config:

```python
config = {
    # Specify which DOM backing engine to use.
    'engine': DOM.HTML5LIB,
    # Or for lxml:
    'engine': DOM.LXML,
}
```

### Custom backing engines

The exporter supports using custom engines to generate its output via the `DOM` API.
This feature is only used for development at the moment, if you have a use case for this in production we would love to hear from you. Please get in touch!

Here is an example implementation:

```python
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


exporter = HTML({
    # Use the dotted module syntax to point to the DOMEngine implementation.
    'engine': 'myproject.example.DOMListTree'
})
```

## Contributing

See anything you like in here? Anything missing? We welcome all support, whether on bug reports, feature requests, code, design, reviews, tests, documentation, and more. Please have a look at our [contribution guidelines](.github/CONTRIBUTING.md).

If you just want to set up the project on your own computer, the contribution guidelines also contain all of the setup commands.

## Credits

This project is made possible by the work of [Springload](https://github.com/springload), a New Zealand digital agency, and. The _beautiful_ demo site is the work of [@thibaudcolas](https://github.com/thibaudcolas).

View the full list of [contributors](https://github.com/springload/draftjs_exporter/graphs/contributors). [MIT](https://github.com/springload/draftjs_exporter/blob/master/LICENSE) licensed.
