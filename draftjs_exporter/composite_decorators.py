from __future__ import absolute_import, unicode_literals

import cgi
import re


class CompositeDecorator():

    # Override this to describe the pattern to be replaced
    SEARCH_RE = re.compile('$^')

    # Implemente this to generate a html string to replace the matched text
    def replace(self, match):
        raise NotImplementedError

    def process(self, text, parent=None):
        self.parent = parent
        result = ""
        begin = final = 0
        for i in self.SEARCH_RE.finditer(text):
            begin, end = i.span()
            # append other content
            result += text[final:begin]
            # append replaced content
            result += self.replace(i)
            final = end

        result += text[final:]
        return result


class URLDecorator(CompositeDecorator):
    """
    replace url in plain text to actual html link
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def __init__(self, new_window=False):
        self.new_window = new_window

    def __repr__(self):
        return '<URLDecorator>'

    def replace(self, match):
        result = ""
        u_protocol = match.group(1)
        u_href = match.group(2)
        u_href = u_protocol + u_href
        if self.parent and self.parent.name == 'a':
            return u_href

        text = cgi.escape(u_href)
        if u_href.startswith("www"):
            u_href = "http://" + u_href
        result = '<a href="{href}"{target}>{text}</a>'.format(
            href=u_href,
            text=text,
            target='target="_blank"' if self.new_window else '')

        return result
