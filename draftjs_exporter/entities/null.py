from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM


class Null():
    def render(self):
        return DOM.create_element()
