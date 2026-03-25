from draftjs_exporter.markdown.helpers import block, inline
from draftjs_exporter.markdown.lists import list_item, make_numbered_li_prefix
from draftjs_exporter.types import Component, Element, Props


def prefixed_block(prefix: str) -> Component:
    return lambda props: block([prefix, props["children"]])


def make_ul(marker: str) -> Component:
    prefix = f"{marker} "
    return lambda props: list_item(prefix, props)


def make_ol(delimiter: str) -> Component:
    get_prefix = make_numbered_li_prefix(delimiter)
    return lambda props: list_item(get_prefix(props), props)


def list_wrapper(props: Props) -> Element:
    return inline([])


ul: Component = make_ul("-")
ol: Component = make_ol(".")
