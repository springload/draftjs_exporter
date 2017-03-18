# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import codecs
import cProfile
import re
from pstats import Stats

# draftjs_exporter provides default configurations and predefined constants for reuse.
from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML


def Blockquote(props):
    block_data = props['block']['data']

    return DOM.create_element('blockquote', {
        'cite': block_data.get('cite')
    }, props['children'])


def ListItem(props):
    depth = props['block']['depth']

    return DOM.create_element('li', {
        'class': 'list-item--depth-{0}'.format(depth)
    }, props['children'])


def OrderedList(props):
    depth = props['block']['depth']

    return DOM.create_element('ol', {
        'class': 'list--depth-{0}'.format(depth)
    }, props['children'])


def Image(props):
    return DOM.create_element('img', {
        'src': props.get('src'),
        'width': props.get('width'),
        'height': props.get('height'),
        'alt': props.get('alt'),
    })


class Link:
    def __init__(self, use_new_window=False):
        self.use_new_window = use_new_window

    def render(self, props):
        link_props = {
            'href': props['url'],
        }

        if self.use_new_window:
            link_props['target'] = '_blank'
            link_props['rel'] = 'noreferrer noopener'

        return DOM.create_element('a', link_props, props['children'])


class BR:
    """
    Replace line breaks (\n) with br tags.
    """
    SEARCH_RE = re.compile(r'\n')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('br')


class Hashtag:
    """
    Wrap hashtags in spans with a specific class.
    """
    SEARCH_RE = re.compile(r'#\w+')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('span', {'class': 'hashtag'}, props['children'])


class Linkify:
    """
    Wrap plain URLs with link tags.
    See http://pythex.org/?regex=(http%3A%2F%2F%7Chttps%3A%2F%2F%7Cwww%5C.)(%5Ba-zA-Z0-9%5C.%5C-%25%2F%5C%3F%26_%3D%5C%2B%23%3A~!%2C%5C%27%5C*%5C%5E%24%5D%2B)&test_string=search%20http%3A%2F%2Fa.us%20or%20https%3A%2F%2Fyahoo.com%20or%20www.google.com%20for%20%23github%20and%20%23facebook&ignorecase=0&multiline=0&dotall=0&verbose=0
    for an example.
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def render(self, props):
        match = props.get('match')
        protocol = match.group(1)
        url = match.group(2)
        href = protocol + url

        if props['block_type'] == BLOCK_TYPES.CODE:
            return href

        link_props = {
            'href': href,
        }

        if href.startswith('www'):
            link_props['href'] = 'http://' + href

        return DOM.create_element('a', link_props, href)


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
            'wrapper': OrderedList,
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

exporter = HTML(config)

content_state = {
    "entityMap": {
        "0": {
            "type": "LINK",
            "mutability": "MUTABLE",
            "data": {
                "url": "https://github.com/facebook/draft-js"
            }
        },
        "1": {
            "type": "LINK",
            "mutability": "MUTABLE",
            "data": {
                "url": "https://facebook.github.io/react/docs/top-level-api.html#react.createelement"
            }
        },
        "2": {
            "type": "HORIZONTAL_RULE",
            "mutability": "IMMUTABLE",
            "data": {}
        },
        "3": {
            "type": "LINK",
            "mutability": "MUTABLE",
            "data": {
                "url": "https://facebook.github.io/react/docs/jsx-in-depth.html"
            }
        },
        "4": {
            "type": "LINK",
            "mutability": "MUTABLE",
            "data": {
                "url": "https://github.com/springload/draftjs_exporter/pull/17"
            }
        },
        "5": {
            "type": "IMAGE",
            "mutability": "IMMUTABLE",
            "data": {
                "alt": "Test image alt text",
                "src": "https://placekitten.com/g/300/200",
                "width": 300,
                "height": 200
            }
        },
        "6": {
            "type": "LINK",
            "mutability": "MUTABLE",
            "data": {
                "url": "http://embed.ly/"
            }
        },
        "7": {
            "type": "EMBED",
            "mutability": "IMMUTABLE",
            "data": {
                "url": "http://www.youtube.com/watch?v=feUYwoLhE_4",
                "title": "React.js Conf 2016 - Isaac Salier-Hellendag - Rich Text Editing with React",
                "providerName": "YouTube",
                "authorName": "Facebook Developers",
                "thumbnail": "https://i.ytimg.com/vi/feUYwoLhE_4/hqdefault.jpg"
            }
        }
    },
    "blocks": [{
        "key": "b0ei9",
        "text": "draftjs_exporter is an HTML exporter for Draft.js content",
        "type": "header-two",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [{
            "offset": 41,
            "length": 8,
            "key": 0
        }],
        "data": {}
    }, {
        "key": "74al",
        "text": "Try it out by running this file!",
        "type": "blockquote",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {
            "cite": "http://example.com/"
        }
    }, {
        "key": "7htbd",
        "text": "Features 📝🍸",
        "type": "header-three",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "32lnv",
        "text": "The exporter aims to provide sensible defaults from basic block types and inline styles to HTML, that can easily be customised when required. For more advanced scenarios, an API is provided (mimicking React's createElement) to create custom rendering components of arbitrary complexity.",
        "type": "unstyled",
        "depth": 0,
        "inlineStyleRanges": [{
            "offset": 209,
            "length": 13,
            "style": "CODE"
        }],
        "entityRanges": [{
            "offset": 209,
            "length": 13,
            "key": 1
        }],
        "data": {}
    }, {
        "key": "eqjvu",
        "text": " ",
        "type": "atomic",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [{
            "offset": 0,
            "length": 1,
            "key": 2
        }],
        "data": {}
    }, {
        "key": "9fr0j",
        "text": "Here are some features worth highlighting:",
        "type": "unstyled",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "2mhgt",
        "text": "Convert line breaks to <br>\nelements.",
        "type": "unordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [{
            "offset": 23,
            "length": 4,
            "style": "CODE"
        }],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "f4gp0",
        "text": "Automatic conversion of entity data to HTML attributes (int & boolean to string, className to class).",
        "type": "unordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [{
            "offset": 81,
            "length": 9,
            "style": "CODE"
        }, {
            "offset": 94,
            "length": 5,
            "style": "CODE"
        }],
        "entityRanges": [{
            "offset": 81,
            "length": 18,
            "key": 3
        }],
        "data": {}
    }, {
        "key": "3cnm0",
        "text": "Wrapped blocks (<li> elements go inside <ul> or <ol>).",
        "type": "unordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [{
            "offset": 16,
            "length": 5,
            "style": "CODE"
        }, {
            "offset": 40,
            "length": 4,
            "style": "CODE"
        }, {
            "offset": 48,
            "length": 4,
            "style": "CODE"
        }],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "h5rn",
        "text": "With arbitrary nesting.",
        "type": "unordered-list-item",
        "depth": 1,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "5qfeb",
        "text": "Common text styles: Bold, Italic, Underline, Monospace, Strikethrough. cmd + b",
        "type": "unordered-list-item",
        "depth": 2,
        "inlineStyleRanges": [{
            "offset": 20,
            "length": 4,
            "style": "BOLD"
        }, {
            "offset": 26,
            "length": 6,
            "style": "ITALIC"
        }, {
            "offset": 34,
            "length": 9,
            "style": "UNDERLINE"
        }, {
            "offset": 45,
            "length": 9,
            "style": "CODE"
        }, {
            "offset": 56,
            "length": 14,
            "style": "STRIKETHROUGH"
        }, {
            "offset": 71,
            "length": 7,
            "style": "KBD"
        }],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "2ol8n",
        "text": "Overlapping text styles. Custom styles too!",
        "type": "unordered-list-item",
        "depth": 2,
        "inlineStyleRanges": [{
            "offset": 0,
            "length": 14,
            "style": "STRIKETHROUGH"
        }, {
            "offset": 12,
            "length": 4,
            "style": "BOLD"
        }, {
            "offset": 14,
            "length": 11,
            "style": "ITALIC"
        }, {
            "offset": 25,
            "length": 13,
            "style": "HIGHLIGHT"
        }],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "2lno0",
        "text": "#hashtag support via #CompositeDecorators.",
        "type": "unordered-list-item",
        "depth": 3,
        "inlineStyleRanges": [],
        "entityRanges": [{
            "offset": 21,
            "length": 20,
            "key": 4
        }],
        "data": {}
    }, {
        "key": "37n0m",
        "text": "Linkify URLs too! http://example.com/",
        "type": "unordered-list-item",
        "depth": 4,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "37n01",
        "text": "Depth can go back and forth, it works fiiine (1)",
        "type": "unordered-list-item",
        "depth": 2,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "37n02",
        "text": "Depth can go back and forth, it works fiiine (2)",
        "type": "unordered-list-item",
        "depth": 1,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "37n03",
        "text": "Depth can go back and forth, it works fiiine (3)",
        "type": "unordered-list-item",
        "depth": 2,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "37n04",
        "text": "Depth can go back and forth, it works fiiine (4)",
        "type": "unordered-list-item",
        "depth": 1,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "37n05",
        "text": "Depth can go back and forth, it works fiiine (5)",
        "type": "unordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "3tbpg",
        "text": " ",
        "type": "atomic",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [{
            "offset": 0,
            "length": 1,
            "key": 5
        }],
        "data": {}
    }, {
        "key": "f7s8c",
        "text": " ",
        "type": "atomic",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [{
            "offset": 0,
            "length": 1,
            "key": 7
        }],
        "data": {}
    }, {
        "key": "5t6c9",
        "text": "For developers 🚀",
        "type": "header-three",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "2nb2a",
        "text": "Import the library",
        "type": "ordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "cfom5",
        "text": "Define your configuration",
        "type": "ordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "e2114",
        "text": "Go!",
        "type": "ordered-list-item",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "adt4j",
        "text": "Optionally, define your custom components.",
        "type": "ordered-list-item",
        "depth": 1,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "ed7hu",
        "text": "def Blockquote(props):\n    block_data = props['block']['data']\n    return DOM.create_element('blockquote', {\n        'cite': block_data.get('cite')\n    }, props['children'])\n",
        "type": "code-block",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }, {
        "key": "1nols",
        "text": "Voilà!",
        "type": "unstyled",
        "depth": 0,
        "inlineStyleRanges": [],
        "entityRanges": [],
        "data": {}
    }]
}

pr = cProfile.Profile()
pr.enable()

html = exporter.render(content_state)

pr.disable()
p = Stats(pr)

pretty = DOM.pretty_print(html)

# Display in console.
print(pretty)

p.strip_dirs().sort_stats('cumulative').print_stats(0)

styles = """
/* Tacit CSS framework https://yegor256.github.io/tacit/ */
input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}th{font-weight:600}td,th{border-bottom:1.08px solid #ccc;padding:14.85px 18px}thead th{border-bottom-width:2.16px;padding-bottom:6.3px}table{display:block;max-width:100%;overflow-x:auto}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}input,textarea,select,button{display:block;max-width:100%;padding:9.9px}label{display:block;margin-bottom:14.76px}input[type="submit"],input[type="reset"],button{background:#f2f2f2;border-radius:3.6px;color:#8c8c8c;cursor:pointer;display:inline;margin-bottom:18px;margin-right:7.2px;padding:6.525px 23.4px;text-align:center}input[type="submit"]:hover,input[type="reset"]:hover,button:hover{background:#d9d9d9;color:#000}input[type="submit"][disabled],input[type="reset"][disabled],button[disabled]{background:#e6e6e6;color:#b3b3b3;cursor:not-allowed}input[type="submit"],button[type="submit"]{background:#367ac3;color:#fff}input[type="submit"]:hover,button[type="submit"]:hover{background:#255587;color:#bfbfbf}input[type="text"],input[type="password"],input[type="email"],input[type="url"],input[type="phone"],input[type="tel"],input[type="number"],input[type="datetime"],input[type="date"],input[type="month"],input[type="week"],input[type="color"],input[type="time"],input[type="search"],input[type="range"],input[type="file"],input[type="datetime-local"],select,textarea{border:1px solid #ccc;margin-bottom:18px;padding:5.4px 6.3px}input[type="checkbox"],input[type="radio"]{float:left;line-height:36px;margin-right:9px;margin-top:8.1px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}pre,code,kbd,samp,var,output{font-family:Menlo,Monaco,Consolas,"Courier New",monospace;font-size:16.2px}pre{border-left:1.8px solid #96bbe2;line-height:25.2px;margin-top:29.7px;overflow:auto;padding-left:18px}pre code{background:none;border:0;line-height:29.7px;padding:0}code{background:#ededed;border:1.8px solid #ccc;border-radius:3.6px;display:inline-block;line-height:18px;padding:3px 6px 2px}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}h1,h2,h3,h4,h5,h6{color:#000;margin-bottom:18px}h1{font-size:36px;font-weight:500;margin-top:36px}h2{font-size:25.2px;font-weight:400;margin-top:27px}h3{font-size:21.6px;margin-top:21.6px}h4{font-size:18px;margin-top:18px}h5{font-size:14.4px;font-weight:bold;margin-top:18px;text-transform:uppercase}h6{color:#ccc;font-size:14.4px;font-weight:bold;margin-top:18px;text-transform:uppercase}input,textarea,select,button,html,body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:18px;font-stretch:normal;font-style:normal;font-weight:300;line-height:29.7px}a{color:#367ac3;text-decoration:none}a:hover{text-decoration:underline}hr{border-bottom:1px solid #ccc}small{font-size:15.3px}em,i{font-style:italic}strong,b{font-weight:600}*{border:0;border-collapse:separate;border-spacing:0;box-sizing:border-box;margin:0;outline:0;padding:0;text-align:left;vertical-align:baseline}html,body{height:100%;width:100%}body{background:#f5f5f5;color:#1a1a1a;padding:36px}p,ul,ol,dl,blockquote,hr,pre,table,form,fieldset,figure,address{margin-bottom:29.7px}section{margin-left:auto;margin-right:auto;max-width:100%;width:900px}article{background:#fff;border:1.8px solid #d9d9d9;border-radius:7.2px;padding:43.2px}header{margin-bottom:36px}footer{margin-top:36px}nav{text-align:center}nav ul{list-style:none;margin-left:0;text-align:center}nav ul li{display:inline;margin-left:9px;margin-right:9px}nav ul li:first-child{margin-left:0}nav ul li:last-child{margin-right:0}ol,ul{margin-left:29.7px}li ol,li ul{margin-bottom:0}@media (max-width: 767px){body{padding:18px}article{border-radius:0;margin:-18px;padding:18px}textarea,input,select{max-width:100%}fieldset{min-width:0}section{width:auto}fieldset,x:-moz-any-link{display:table-cell}}
/* Custom styles to help with debugging */
blockquote { border-left: 0.25rem solid #aaa; padding-left: 1rem; font-style: italic; }
.u-text-center { text-align: center; }
a:hover, a:focus { outline: 1px solid red; }
.hashtag { color: pink; }
.list-item--depth-1 { margin-left: 5rem; }
"""

# Output to a styled HTML file for development.
with codecs.open('example.html', 'w', 'utf-8') as file:
    file.write("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>draftjs_exporter test page</title>
<style>{styles}</style>
</head>
<body>
    {html}
</body>
</html>
""".format(styles=styles, html=html))

# Output to a Markdown file to showcase the output in GitHub (and see changes in git).
with codecs.open('docs/example.md', 'w', 'utf-8') as file:
    file.write("""
# Example output (generated by [`example.py`](../example.py))

-----
{html}
-----
""".format(html=html))
