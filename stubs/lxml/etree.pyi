from typing import (
    Dict,
    Optional,
)
from typing_extensions import Literal


Attrib = Optional[Dict[str, str]]
NSMap = Optional[Dict[Literal['xlink'], Literal['http://www.w3.org/1999/xlink']]]


class Element():
    def __init__(self, _tag: str, attrib: Attrib = ..., nsmap: NSMap = ...): ...  # noqa: E704

    def append(self, child: 'Element') -> None: ...  # noqa: E704


def tostring(elt: Element, method: Literal['html'], encoding: Literal['unicode']) -> str: ...  # noqa: E704
