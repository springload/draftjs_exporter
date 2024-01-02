from typing import (
    Dict,
    Optional,
)

Attrib = Optional[Dict[str, str]]
NSMap = Optional[Dict[str, str]]

class Element:
    text: Optional["Element"] = None
    def __init__(self, _tag: str, attrib: Attrib = ..., nsmap: NSMap = ...): ...
    def append(self, child: "Element") -> None: ...

def tostring(elt: Element, method: str, encoding: str) -> str: ...
