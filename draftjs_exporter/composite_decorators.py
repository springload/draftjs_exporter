from __future__ import absolute_import, unicode_literals

from operator import itemgetter
from draftjs_exporter.dom import DOM


def get_decorations(decorators, text):
    occupied = {}
    decorations = []

    for deco in decorators:
        for match in deco.SEARCH_RE.finditer(text):
            begin, end = match.span()
            if not any(occupied.get(i) for i in range(begin, end)):
                for i in range(begin, end):
                    occupied[i] = 1
                decorations.append((begin, end, match, deco))

    decorations.sort(key=itemgetter(0))

    return decorations


def apply_decorators(decorators, text, block_type):
    decorations = get_decorations(decorators, text)

    pointer = 0
    for begin, end, match, decorator in decorations:
        if pointer < begin:
            yield DOM.create_text_node(text[pointer:begin])

        yield decorator.render({
            'children': match.group(0),
            'match': match,
            'block_type': block_type,
        })
        pointer = end

    if pointer < len(text):
        yield DOM.create_text_node(text[pointer:])


def render_decorators(decorators, text, block_type):
    decorated_node = DOM.create_document_fragment()

    for decorated_child in apply_decorators(decorators, text, block_type):
        DOM.append_child(decorated_node, decorated_child)

    return decorated_node
