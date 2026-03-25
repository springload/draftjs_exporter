import logging

from draftjs_exporter.markdown.helpers import block
from draftjs_exporter.types import Element, Props

logger = logging.getLogger(__name__)


def block_fallback(props: Props) -> Element:
    type_ = props["block"]["type"]
    logger.warning('Unknown block type "%s". Rendering as plain text.', type_)
    return block([props["children"]])


def entity_fallback(props: Props) -> Element:
    type_ = props["entity"]["type"]
    logger.warning('Unknown entity type "%s". Rendering as plain text.', type_)
    return props["children"]


def style_fallback(props: Props) -> Element:
    type_ = props["inline_style_range"]["style"]
    logger.warning('Unknown inline style "%s". Rendering as plain text.', type_)
    return props["children"]
