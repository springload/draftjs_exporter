from draft_exporter.html import DraftJsExporter
from draft_exporter.entities.link import Link


config = {
    'entity_decorators': {
        'LINK': Link
    },
    'block_map': {
        'header-one': {'element': 'h1'},
        'unordered-list-item': {
            'element': 'li',
            'wrapper': ['ul', {'className': 'public-DraftStyleDefault-ul'}]
        },
        'unstyled': {'element': 'div'}
    },
    'style_map': {
        'ITALIC': {'fontStyle': 'italic'},
        'BOLD': {'fontStyle': 'bold'}
    }
}

exporter = DraftJsExporter(config)

content_state = {
    'entityMap': {
        '0': {
            'type': 'LINK',
            'mutability': 'MUTABLE',
            'data': {
                'url': 'http://example.com'
            }
        }
    },
    'blocks': [
        {
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [{
                'offset': 0,
                'length': 2,
                'style': 'BOLD'
            }],
            'entityRanges': []
        },
        {
            'key': 'dem5p',
            'text': 'some paragraph text',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [
                {
                    'offset': 0,
                    'length': 4,
                    'style': 'ITALIC'
                }
            ],
            'entityRanges': [
                {
                    'offset': 5,
                    'length': 9,
                    'key': 0
                }
            ]
        }
    ]
}


markup = exporter.call(content_state)
print (markup)
