import re
from collections.abc import Callable
from typing import Any, Literal, TypedDict

# Element represents an instance of a RenderableType. It’s engine-specific so very hard to type.
Element = Any
# Props are always a dictionary with string keys and arbitrary values.
Props = dict[str, Any]

# A DOM tag name.
Tag = str
# A component function, taking props as a parameter and returning an Element by calling DOM.create_element.
Component = Callable[[Props], Element]
# What can be rendered: None, DOM tag name, Component.
RenderableType = Component | Tag | None
# The output of the exporter.
HTML = str


# Config for a single renderable, element and optional wrappers / props.
class RenderableConfig(TypedDict, total=False):
    element: RenderableType
    props: Props
    wrapper: RenderableType
    wrapper_props: Props


# block_map, style_map, entity_decorators.
ConfigMap = dict[str, RenderableConfig | RenderableType]


# composite_decorators.
class Decorator(TypedDict):
    strategy: re.Pattern[str]
    component: RenderableType


CompositeDecorators = list[Decorator]


# The whole config object.
class Config(TypedDict, total=False):
    block_map: ConfigMap
    style_map: ConfigMap
    entity_decorators: ConfigMap
    composite_decorators: CompositeDecorators
    engine: str


# Blocks have a predetermined set of keys and values, but let’s be permissive.
class InlineStyleRange(TypedDict):
    offset: int
    length: int
    style: str


class EntityRange(TypedDict):
    offset: int
    length: int
    key: int


class Block(TypedDict, total=False):
    key: str
    text: str
    type: str
    depth: int
    data: dict[str, Any]
    inlineStyleRanges: list[InlineStyleRange]
    entityRanges: list[EntityRange]


# Entity key is int in blocks, str in Entity map.
EntityKey = str

Mutability = Literal["MUTABLE", "IMMUTABLE", "SEGMENTED"]


class EntityDetails(TypedDict, total=False):
    type: str
    data: dict[str, Any]
    mutability: Mutability


EntityMap = dict[EntityKey, EntityDetails]


# The whole content state. blocks and entity_map.
class ContentState(TypedDict, total=False):
    blocks: list[Block]
    entityMap: EntityMap
