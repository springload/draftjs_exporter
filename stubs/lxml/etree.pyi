from typing import Dict

Attrib = Dict[str, str] | None
NSMap = Dict[str, str] | None

class Element:
    text: "Element" | None = None
    def __init__(self, _tag: str, attrib: Attrib = ..., nsmap: NSMap = ...): ...
    def append(self, child: "Element") -> None: ...

def tostring(elt: Element, method: str, encoding: str) -> str: ...
