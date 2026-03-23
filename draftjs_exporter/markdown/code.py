from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.lists import get_li_suffix
from draftjs_exporter.types import Element, Props


def code_element(props: Props) -> Element:
    suffix = get_li_suffix(props)
    block_end = "\n```" if suffix == "\n\n" else ""

    return DOM.create_element("fragment", {}, [props["children"], block_end, suffix])


def code_wrapper(props: Props) -> Element:
    return DOM.create_element("fragment", {}, ["```\n"])
