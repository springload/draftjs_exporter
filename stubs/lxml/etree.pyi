from typing import (
    Dict,
    Optional,
)


Attrib = Optional[Dict[str, str]]
NSMap = Optional[Dict[str, str]]


class Element():
    text = None  # type: Optional['Element']

    def __init__(self, _tag: str, attrib: Attrib = ..., nsmap: NSMap = ...): ...  # noqa: E704

    def append(self, child: 'Element') -> None: ...  # noqa: E704


def tostring(elt: Element, method: str, encoding: str) -> str: ...  # noqa: E704
