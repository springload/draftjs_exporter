Changelog
=========

> All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [[v0.4.0]](https://github.com/springload/draftjs_exporter/releases/tag/v0.4.0) - 2016-10-15

This release is likely to be a **breaking change**. It is not released as such because the exporter has not [reached 1.0 yet](http://semver.org/#spec-item-4).

### Changed

- Now using [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and the [html5lib](https://github.com/html5lib/html5lib-python) parser instead of lxml.
- Entities are now available from `draftjs_exporter.entities` instead of `draftjs_exporter.entities.<entity>`

### Added

- Support for simpler `wrapper` options definition: `{'unordered-list-item' : { 'element': 'li', 'wrapper': 'ul'}}`
- Support for options definition for every element, not just wrappers: `{'header-two' : { 'element': ['h2', {'className': 'c-amazing-heading'}]}}`
- Support for None in the children of an element in `DOM.create_element`, for conditional rendering like what React does.
- Support for entity class in `DOM.create_element`.

### Fixed

- Fix behavior of wrapper stack in nested wrappers ([#15](https://github.com/springload/draftjs_exporter/issues/15))

## [[v0.3.3]](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.3) - 2016-10-06

Last release before switching to BeautifulSoup4 / html5lib. If we ever need to switch back to lxml, it should be as simple as looking at the code at [v0.3.3](https://github.com/springload/draftjs_exporter/tree/v0.3.3).

### Added

- Add wrapper method to create new elements.
- Add wrapper method to retrieve an element's list of classes.

## [[v0.3.2]](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.2) - 2016-07-25

### Fixed

- Fix exporter crashing on empty blocks (renders empty string instead)

## [[v0.3.1]](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.1) - 2016-07-20

### Fixed

- Use HTML parser instead of XML for DOM API

## [[v0.3.0]](https://github.com/springload/draftjs_exporter/releases/tag/v0.3.0) - 2016-07-20

### Added

- Automatic conversion of entity data to HTML attributes (int & boolean to string, `className` to `class`).
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

## [[v0.2.0]](https://github.com/springload/draftjs_exporter/releases/tag/v0.2.0) - 2016-07-05

### Added

- Support for `<hr/>` tag / `TOKEN` entities
- Support for wrapped item nesting (arbitrary depth)

## [[v0.1.0]](https://github.com/springload/draftjs_exporter/releases/tag/v0.1.0) - 2016-07-04

First usable release!

-------------

## [[x.y.z]](https://github.com/springload/draftjs_exporter/releases/tag/x.y.z) - YYYY-MM-DD (Template: http://keepachangelog.com/)

### Added

- Something was added to the API / a new feature was introduced.

### Changed

### Fixed

### Removed
