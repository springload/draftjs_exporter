from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM


class Null():
    def render(self, props):
        return DOM.create_element()
