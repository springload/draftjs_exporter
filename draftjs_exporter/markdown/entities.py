from draftjs_exporter.markdown.helpers import block, inline
from draftjs_exporter.types import Element, Props


def image(props: Props) -> Element:
    return block(["![", props.get("alt", ""), "](", props["src"], ")"])


def link(props: Props) -> Element:
    return inline(["[", props["children"], "](", props["url"], ")"])


def horizontal_rule(props: Props) -> Element:
    return block(["---"])
