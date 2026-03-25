from draftjs_exporter.markdown.helpers import block, inline
from draftjs_exporter.types import Component, Element, Props


def image(props: Props) -> Element:
    return block(["![", props.get("alt", ""), "](", props["src"], ")"])


def link(props: Props) -> Element:
    return inline(["[", props["children"], "](", props["url"], ")"])


def make_horizontal_rule(marker: str) -> Component:
    return lambda props: block([marker])


horizontal_rule: Component = make_horizontal_rule("---")
