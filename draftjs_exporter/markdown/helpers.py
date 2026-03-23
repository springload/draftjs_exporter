from draftjs_exporter.dom import DOM
from draftjs_exporter.types import Element


def inline(children: list[str | Element]) -> Element:
    """Inline formatting, eg. bold, links, code."""
    return DOM.create_element("fragment", {}, children)


def block(children: list[str | Element]) -> Element:
    """Block formatting. In Markdown, blocks are followed by an empty line."""
    return DOM.create_element("fragment", {}, children + ["\n\n"])
