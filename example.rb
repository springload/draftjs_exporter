require 'draftjs_exporter/entities/link'
require 'draftjs_exporter/html'

config = {
  entity_decorators: {
    'LINK' => DraftjsExporter::Entities::Link.new
  },
  block_map: {
    'header-one' => { element: 'h1' },
    'unordered-list-item' => {
      element: 'li',
      wrapper: ['ul', { className: 'public-DraftStyleDefault-ul' }]
    },
    'unstyled' => { element: 'div' }
  },
  style_map: {
    'ITALIC' => { fontStyle: 'italic'},
  }
}

# New up the exporter
exporter = DraftjsExporter::HTML.new(config)

# Provide raw content state
puts exporter.call({
  entityMap: {
    '0' => {
      type: 'LINK',
      mutability: 'MUTABLE',
      data: {
        url: 'http://example.com'
      }
    }
  },
  blocks: [
    {
      key: '5s7g9',
      text: 'Header',
      type: 'header-one',
      depth: 0,
      inlineStyleRanges: [],
      entityRanges: []
    },
    {
      key: 'dem5p',
      text: 'some paragraph text',
      type: 'unstyled',
      depth: 0,
      inlineStyleRanges: [
        {
          offset: 0,
          length: 4,
          style: 'ITALIC'
        }
      ],
      entityRanges: [
        {
          offset: 5,
          length: 9,
          key: 0
        }
      ]
    }
  ]
})
