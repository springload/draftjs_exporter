# Changelog

> All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.9.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.9.0)

### Added

- Add configuration options to determine handling of missing blocks #52.
- Add configuration options to determine handling of missing styles.
- Add configuration options to determine handling of missing entities.
- Block components now have access to the block type via `props['block']['type']`.
- Entity components now have access to the entity type via `props['entity']['type']`.
- Composite decorators now have access to the current block depth and data via `props['block']['depth']`, `props['block']['data']`.
- Allow discarding component children by returning `None` in `render`.
- Add support for `lxml` as a DOM backing engine, with `pip install draftjs_exporter[lxml]` pip extra.
- Add support for custom DOM backing engines.
- Add support for None content state in HTML.render #67.

### Changed

- For composite decorators, the block type has moved from `props['block_type']` to `props['block']['type']`.
- Move `ConfigException` to `draftjs_exporter.error`.

### Removed

- Remove `DOM.get_children` method.
- Remove `DOM.pretty_print` method.
- Remove automatic conversion from `className` prop to `class`.

### Fixed

- Stop rendering decorators when there is no text to decorate.
- Remove extra HTML serialisation steps.

### How to upgrade

```diff
# Change composite decorators block type access
- props['block_type']
+ props['block']['type']
# Stop using DOM.get_children directly.
- DOM.get_children()
# Stop using DOM.pretty_print directly.
- DOM.pretty_print()
# Move `ConfigException` to `draftjs_exporter.error`.
- from draftjs_exporter.options import ConfigException
+ from draftjs_exporter.error import ConfigException
# Remove automatic conversion from `className` prop to `class` attribute.
- BLOCK_TYPES.BLOCKQUOTE: ['blockquote', {'className': 'c-pullquote'}]
+ BLOCK_TYPES.BLOCKQUOTE: ['blockquote', {'class': 'c-pullquote'}]
```

## [v0.8.1](https://github.com/springload/draftjs_exporter/releases/tag/v0.8.1)

### Fixed

- Fix KeyError when the content state is empty.

## [v0.8.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.8.0)

### Added

- Add simplified block mapping format: `BLOCK_TYPES.HEADER_TWO: 'h2'`.
- Raise exception when `style_map` does not define an `element` for the style.
- Add support for any props on `style_map`.
- Automatically convert `style` prop from a dict of camelCase properties to a string, on all elements (if `style` is already a string, it will be output as is).
- Support components (`render` function returning `create_element` nodes) in `style_map`.
- Add more defaults in the style map:

```python
BOLD = 'strong'
CODE = 'code'
ITALIC = 'em'
UNDERLINE = 'u'
STRIKETHROUGH = 's'
SUPERSCRIPT = 'sup'
SUBSCRIPT = 'sub'
MARK = 'mark'
QUOTATION = 'q'
SMALL = 'small'
SAMPLE = 'samp'
INSERT = 'ins'
DELETE = 'del'
KEYBOARD = 'kbd'
```

- Add new `pre` block type.
- Support components (`render` function returning `create_element` nodes) in `block_map`, for both `element` and `wrapper`.

### Removed

- Remove array-style block element and wrapper declarations (`['ul']`, `['ul', {'class': 'bullet-list'}]`).
- Remove `DOM.create_text_node` method.

### Changed

- Replace array-style mapping declarations of block element and wrapper props with `props` and `wrapper_props` attributes (dictionaries of props).
- Moved and renamed `BlockException` to `ConfigException`.
- Replace `style_map` config format to the one of the `block_map`.
- Move internal `camel_to_dash` method to `DOM` for official use.
- Change ordering of inline styles - now using alphabetical ordering of style key instead of tag name.
- `STRIKETHROUGH` styles in default style map now map to `s` tag.
- `UNDERLINE` styles in default style map now map to `u` tag.
- By default, `code-block` blocks are now rendered inside a combination of `pre` and `code` tags.
- For entities, directly pass `data` dict as props instead of whole entity map declaration.

### Fixed

- Fix block ordering with block components and wrapper. Fix #55.

### How to upgrade

```diff
# Change element-only block declarations:
- BLOCK_TYPES.HEADER_TWO: {'element': 'h2'},
+ BLOCK_TYPES.HEADER_TWO: 'h2',
# Change array-style block declarations:
- BLOCK_TYPES.BLOCKQUOTE: ['blockquote', {'class': 'c-pullquote'}]
+ BLOCK_TYPES.BLOCKQUOTE: {'element': 'blockquote', 'props': {'class': 'c-pullquote'}}
# Change block wrapper declarations:
- 'wrapper': ['ul', {'class': 'bullet-list'}],
+ 'wrapper': 'ul',
+ 'wrapper_props': {'class': 'bullet-list'},
# Change location and name of exceptions:
- from draftjs_exporter.wrapper_state import BlockException
+ from draftjs_exporter.options import ConfigException
# Change element-only style declarations:
- 'KBD': {'element': 'kbd'},
+ 'KBD': 'kbd',
# Change object-style style declarations:
- 'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
+ 'HIGHLIGHT': {'element': 'strong', 'props': {'style': {'textDecoration': 'underline'}}},
# Create custom STRIKETHROUGH styles:
+ 'STRIKETHROUGH': {'element': 'span', 'props': {'style': {'textDecoration': 'line-through'}}},
# Create custom UNDERLINE styles:
+ 'UNDERLINE': {'element': 'span', 'props': {'style': {'textDecoration': 'underline'}}},
# New camel_to_dash location:
- from draftjs_exporter.style_state import camel_to_dash
- camel_to_dash()
+ from draftjs_exporter.dom import DOM
+ DOM.camel_to_dash()
# New default rendering for code-block:
- BLOCK_TYPES.CODE: 'pre',
+ BLOCK_TYPES.CODE: lambda props: DOM.create_element('pre', {}, DOM.create_element('code', {}, props['children'])),
# Use the new pre block to produce the previous result, or override the default for code-block.
+ BLOCK_TYPES.PRE: 'pre',
# Entities now receive the content of `data` directly, instead of the whole entity:
  def render(self, props):
-     data = props.get('data', {})
      link_props = {
-         'href': data['url'],
+         'href': props['url'],
      }
# Remove wrapping around text items.
- DOM.create_text_node(text)
+ text
# Remove fragment calls.
- DOM.create_document_fragment()
+ DOM.create_element()
# Remove text getters and setters. This is not supported anymore.
- DOM.get_text_content(elt)
- DOM.set_text_content(elt, text)
```

## [v0.7.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.7.0)

### Added

- Add support for decorators thanks to @su27 (#16, #17).
- Add support for configurable decorators and entities.
- Add support for decorators and entities in function form.

### Changed

- Stop lowercasing HTML attributes. `*ngFor` will now be exported as `*ngFor`.

### Removed

- Drop Python 3.3 support (likely still runs fine, but tests are not ran on it).

## [v0.6.2](https://github.com/springload/draftjs_exporter/releases/tag/v0.6.2)

### Added

- Add profiling tooling thanks to @su27 (#31).
- Add more common entity types in constants (#34).

### Fixed

- Stop mutating entity data when rendering entities (#36).

## [v0.6.1](https://github.com/springload/draftjs_exporter/releases/tag/v0.6.1)

### Added

- Automatically convert line breaks to `br` elements.

## [v0.6.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.6.0)

This release is likely to be a **breaking change**. It is not released as such because the exporter has not [reached 1.0 yet](http://semver.org/#spec-item-4).

### Changed

- Change `hr` rendering to be done with entities instead of block types. Instead of having a `TOKEN` entity rendering as `Null` inside a `horizontal-rule` block rendering as `hr`, we now have a `HORIZONTAL_RULE` entitiy rendering as `HR` inside an `atomic` block rendering as `fragment`.

### Removed

- Remove custom block type `pullquote`

## [v0.5.2](https://github.com/springload/draftjs_exporter/releases/tag/v0.5.2)

### Fixed

- Fix state being kept between exports, causing blocks to be duplicated in re-runs.

## [v0.5.1](https://github.com/springload/draftjs_exporter/releases/tag/v0.5.1)

### Fixed

- Fix broken link in README

## [v0.5.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.5.0)

This release is likely to be a **breaking change**. It is not released as such because the exporter has not [reached 1.0 yet](http://semver.org/#spec-item-4).

### Added

- Add support for more scenarios with nested blocks. Jumping depths eg. 0, 2, 3. Starting directly above 0 eg. 2, 2, 0. Not using 0 at all eg. 3, 3, 3.

### Changed

- Entity decorators now have complete control on where their content (markup, not just text) is inserted into the DOM. This is done via the `children` prop in a similar fashion to React's.

### Removed

- Built-in entities are no longer available as part of the library. They should be defined in userland.

## [v0.4.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.4.0)

This release is likely to be a **breaking change**. It is not released as such because the exporter has not [reached 1.0 yet](http://semver.org/#spec-item-4).

### Changed

- Now using [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and the [html5lib](https://github.com/html5lib/html5lib-python) parser instead of lxml.
- Entities are now available from `draftjs_exporter.entities` instead of `draftjs_exporter.entities.<entity>`

### Added

- Support for simpler `wrapper` options definition: `{'unordered-list-item' : { 'element': 'li', 'wrapper': 'ul'}}`
- Support for options definition for every element, not just wrappers: `{'header-two' : { 'element': ['h2', {'class': 'c-amazing-heading'}]}}`
- Support for None in the children of an element in `DOM.create_element`, for conditional rendering like what React does.
- Support for entity class in `DOM.create_element`.

### Fixed

- Fix behavior of wrapper stack in nested wrappers ([#15](https://github.com/springload/draftjs_exporter/issues/15))

## [v0.3.3](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.3)

Last release before switching to BeautifulSoup4 / html5lib. If we ever need to switch back to lxml, it should be as simple as looking at the code at [v0.3.3](https://github.com/springload/draftjs_exporter/tree/v0.3.3).

### Added

- Add wrapper method to create new elements.
- Add wrapper method to retrieve an element's list of classes.

## [v0.3.2](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.2)

### Fixed

- Fix exporter crashing on empty blocks (renders empty string instead)

## [v0.3.1](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.1)

### Fixed

- Use HTML parser instead of XML for DOM API

## [v0.3.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.0)

### Added

- Automatic conversion of entity data to HTML attributes (int & boolean to string, `class` to `class`).
- Default, extensible block & inline style maps for common HTML elements.
- React-like API to create custom entity decorators.
- DOM API to abstract HTML building code.
- Dynamically generate test cases from JSON fixture
- Raise exception for undefined entity decorators

### Changed

- (Breaking change) Exporter API changed to be closer to React's
- (Breaking change) Entity decorator API changed to be closer to React's

### Fixed

- Nested blocks backtracking creating multiple wrappers at the same depths instead of reusing existing ones ([#9](https://github.com/springload/draftjs_exporter/issues/9))

### Removed

- Removed Token entity (identical as Null)

## [v0.2.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.2.0)

### Added

- Support for `<hr/>` tag / `TOKEN` entities
- Support for wrapped item nesting (arbitrary depth)

## [v0.1.0](https://github.com/springload/draftjs_exporter/releases/tag/v0.1.0)

First usable release!

-------------

## [vx.y.z](https://github.com/springload/draftjs_exporter/releases/tag/x.y.z) (Template: http://keepachangelog.com/)

### Added

- Something was added to the API / a new feature was introduced.

### Changed

### Fixed

### Removed

### How to upgrade
