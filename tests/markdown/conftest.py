import pytest

from draftjs_exporter.dom import DOM


@pytest.fixture(autouse=True)
def _use_markdown_engine():
    with DOM.engine(DOM.MARKDOWN):
        yield
