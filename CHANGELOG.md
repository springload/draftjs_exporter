# Changelog

> All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
- Support for options definition for every element, not just wrappers: `{'header-two' : { 'element': ['h2', {'className': 'c-amazing-heading'}]}}`
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
