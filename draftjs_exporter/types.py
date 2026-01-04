import re
from collections.abc import Callable
from typing import Any, Literal, TypeAlias, TypedDict

# Element represents an instance of a RenderableType. It’s engine-specific so very hard to type.
Element: TypeAlias = Any
# Props are always a dictionary with string keys and arbitrary values.
Props: TypeAlias = dict[str, Any]

# A DOM tag name.
Tag: TypeAlias = str
# A component function, taking props as a parameter and returning an Element by calling DOM.create_element.
Component: TypeAlias = Callable[[Props], Element]
# What can be rendered: None, DOM tag name, Component.
RenderableType: TypeAlias = Component | Tag | None
# The output of the exporter.
HTML = str


# Config for a single renderable, element and optional wrappers / props.
class RenderableConfig(TypedDict, total=False):
    # TODO Use typing.Required when dropping Python 3.10 support.
    # See https://peps.python.org/pep-0655/.
    element: RenderableType
    props: Props
    wrapper: RenderableType
    wrapper_props: Props


# TODO Introduce a type guard when support improves.
# def is_renderable_config(val: dict) -> TypeGuard[RenderableConfig]:
#     return isinstance(val, dict) and "element" in val

# block_map, style_map, entity_decorators.
ConfigMap: TypeAlias = dict[str, RenderableConfig | RenderableType]


# composite_decorators.
class Decorator(TypedDict):
    strategy: re.Pattern[str]
    component: RenderableType


CompositeDecorators: TypeAlias = list[Decorator]


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
EntityKey: TypeAlias = str

Mutability: TypeAlias = Literal["MUTABLE", "IMMUTABLE", "SEGMENTED"]


class Entity(TypedDict, total=False):
    type: str
    data: dict[str, Any]
    mutability: Mutability


EntityMap: TypeAlias = dict[EntityKey, Entity]


# The whole content state. blocks and entity_map.
class ContentState(TypedDict, total=False):
    blocks: list[Block]
    entityMap: EntityMap
