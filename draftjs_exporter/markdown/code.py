from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.lists import get_li_suffix
from draftjs_exporter.types import Component, Element, Props


def make_code_element(fence: str) -> Component:
    def element(props: Props) -> Element:
        suffix = get_li_suffix(props)
        block_end = f"\n{fence}" if suffix == "\n\n" else ""
        return DOM.create_element(
            "fragment", {}, [props["children"], block_end, suffix]
        )

    return element


def make_code_wrapper(fence: str) -> Component:
    prefix = f"{fence}\n"
    return lambda props: DOM.create_element("fragment", {}, [prefix])


code_element: Component = make_code_element("```")
code_wrapper: Component = make_code_wrapper("```")
