from html import escape

from draftjs_exporter.engines.base import Attr, DOMEngine
from draftjs_exporter.types import HTML, Tag

# http://w3c.github.io/html/single-page.html#void-elements
# https://github.com/html5lib/html5lib-python/blob/0cae52b2073e3f2220db93a7650901f2200f2a13/html5lib/constants.py#L560
VOID_ELEMENTS = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


class Elt:
    """
    A DOM element that the Markdown engine manipulates.
    Identical to the string engine's Elt, but rendering does not escape text.
    """

    __slots__ = ("type", "attr", "children", "markup")

    def __init__(self, type_: Tag, attr: Attr | None, markup: HTML = ""):
        self.type = type_
        self.attr = attr
        self.children: list[str | "Elt"] = []
        self.markup = markup

    @staticmethod
    def from_html(markup: HTML) -> "Elt":
        return Elt("escaped_html", None, markup)


class DOMMarkdown(DOMEngine):
    """
    String concatenation implementation of the DOM API for Markdown output.
    Based on DOMString, but without HTML escaping of text content.
    """

    @staticmethod
    def create_tag(type_: Tag, attr: Attr | None = None) -> Elt:
        return Elt(type_, attr)

    @staticmethod
    def parse_html(markup: HTML) -> Elt:
        return Elt.from_html(markup)

    @staticmethod
    def append_child(elt: Elt, child: str | Elt) -> None:
        # This check is necessary because the current wrapper_state implementation
        # has an issue where it inserts elements multiple times.
        # This must be skipped for text, which can be duplicated.
        is_existing_ref = child in elt.children and isinstance(child, Elt)
        if not is_existing_ref:
            elt.children.append(child)

    @staticmethod
    def render_attrs(attr: Attr) -> str:
        return "".join(sorted([f' {k}="{escape(v)}"' for k, v in attr.items()]))

    @staticmethod
    def render_children(children: list[HTML | Elt]) -> HTML:
        return "".join(
            [DOMMarkdown.render(c) if isinstance(c, Elt) else c for c in children]
        )

    @staticmethod
    def render(elt: Elt) -> HTML:
        type_ = elt.type
        attr = DOMMarkdown.render_attrs(elt.attr) if elt.attr else ""
        children = DOMMarkdown.render_children(elt.children) if elt.children else ""

        match type_:
            case "fragment":
                return children
            case "escaped_html":
                return elt.markup
            case _ if type_ in VOID_ELEMENTS:
                return f"<{type_}{attr}/>"
            case _:
                return f"<{type_}{attr}>{children}</{type_}>"

    @staticmethod
    def render_debug(elt: Elt) -> HTML:
        return DOMMarkdown.render(elt)
