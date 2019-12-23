from typing import Any


class BeautifulSoup():
    def __init__(self, markup: str, features: str) -> None: ...  # noqa: E704

    def prettify(self) -> str: ...  # noqa: E704

    def new_tag(self, type_: str, **attr: Any) -> Any: ...  # noqa: E704
