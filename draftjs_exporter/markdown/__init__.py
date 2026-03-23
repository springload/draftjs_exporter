from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP as HTML_BLOCK_MAP
from draftjs_exporter.defaults import STYLE_MAP as HTML_STYLE_MAP
from draftjs_exporter.html import ExporterConfig
from draftjs_exporter.markdown.blocks import list_wrapper, ol, prefixed_block, ul
from draftjs_exporter.markdown.code import code_element, code_wrapper
from draftjs_exporter.markdown.entities import horizontal_rule, image, link
from draftjs_exporter.markdown.styles import inline_style
from draftjs_exporter.types import ConfigMap

BLOCK_MAP: ConfigMap = {
    **HTML_BLOCK_MAP,
    **{
        BLOCK_TYPES.UNSTYLED: prefixed_block(""),
        BLOCK_TYPES.HEADER_ONE: prefixed_block("# "),
        BLOCK_TYPES.HEADER_TWO: prefixed_block("## "),
        BLOCK_TYPES.HEADER_THREE: prefixed_block("### "),
        BLOCK_TYPES.HEADER_FOUR: prefixed_block("#### "),
        BLOCK_TYPES.HEADER_FIVE: prefixed_block("##### "),
        BLOCK_TYPES.HEADER_SIX: prefixed_block("###### "),
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            "element": ul,
            "wrapper": list_wrapper,
        },
        BLOCK_TYPES.ORDERED_LIST_ITEM: {
            "element": ol,
            "wrapper": list_wrapper,
        },
        BLOCK_TYPES.BLOCKQUOTE: prefixed_block("> "),
        BLOCK_TYPES.CODE: {
            "element": code_element,
            "wrapper": code_wrapper,
        },
    },
}

STYLE_MAP: ConfigMap = dict(
    HTML_STYLE_MAP,
    **{
        INLINE_STYLES.BOLD: inline_style("**"),
        INLINE_STYLES.CODE: inline_style("`"),
        INLINE_STYLES.ITALIC: inline_style("_"),
        INLINE_STYLES.STRIKETHROUGH: inline_style("~"),
    },
)

ENTITY_DECORATORS: ConfigMap = {
    ENTITY_TYPES.IMAGE: image,
    ENTITY_TYPES.LINK: link,
    ENTITY_TYPES.HORIZONTAL_RULE: horizontal_rule,
}

ENGINE = "draftjs_exporter.engines.markdown.DOMMarkdown"

CONFIG: ExporterConfig = {
    "block_map": BLOCK_MAP,
    "style_map": STYLE_MAP,
    "entity_decorators": ENTITY_DECORATORS,
    "engine": ENGINE,
}
