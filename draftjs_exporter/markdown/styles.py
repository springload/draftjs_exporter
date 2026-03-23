from draftjs_exporter.markdown.helpers import inline
from draftjs_exporter.types import Component


def inline_style(mark: str) -> Component:
    return lambda props: inline([mark, props["children"], mark])
