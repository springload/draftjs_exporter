from draftjs_exporter.markdown.helpers import block, inline
from draftjs_exporter.markdown.lists import get_numbered_li_prefix, list_item
from draftjs_exporter.types import Component, Element, Props


def prefixed_block(prefix: str) -> Component:
    return lambda props: block([prefix, props["children"]])


def ul(props: Props) -> Element:
    return list_item("* ", props)


def ol(props: Props) -> Element:
    prefix = get_numbered_li_prefix(props)
    return list_item(prefix, props)


def list_wrapper(props: Props) -> Element:
    return inline([])
