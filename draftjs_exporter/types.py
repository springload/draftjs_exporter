from collections.abc import Callable, Mapping
from typing import Any

# Element represents an instance of a RenderableType. It’s engine-specific so very hard to type.
Element = Any
# Props are always a dictionary with string keys and arbitrary values.
# TODO Other types than string for keys.
Props = dict[str, Any]

# A DOM tag name.
Tag = str
# A component function, taking props as a parameter and returning an Element by calling DOM.create_element.
Component = Callable[[Props], Element]
# What can be rendered: None, DOM tag name, Component.
RenderableType = Component | Tag | None
# The output of the exporter.
HTML = str

# The whole config object.
Config = dict[str, Any]
# block_map, style_map, entity_decorators.
# The dict could be limited to a fixed set of keys, but this would require TypedDict.
ConfigMap = Mapping[str, dict[str, Any] | RenderableType]
# composite_decorators.
Decorator = dict[str, Any]
CompositeDecorators = list[Decorator]

# The whole content state. blocks and entity_map.
ContentState = Mapping[str, Any]
# Blocks have a predetermined set of keys and values, but let’s be permissive without TypedDict.
Block = Mapping[str, Any]
# Entity key is int in blocks, str in Entity map.
EntityKey = str
# Entities have fixed keys.
EntityDetails = Mapping[str, Any]
EntityMap = Mapping[EntityKey, EntityDetails]
