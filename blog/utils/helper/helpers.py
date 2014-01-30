# -*- coding: utf-8 -*-
import re
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    """MLStripper support functions for feed Html.

    This helper will help feed contents from Full html tags content to pure
    content.

    Attributes:
        html: Full html tags content
    """
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class ReHelper(object):

    """ReHelper support muti re functions.

    This helper will support a few muti-used functions for contents that need
    re-place or re-test.
    """

    def __init__(self):
        pass

    def r_slash(self, s):
        """Ensure user submited string not contains '/' or muti '-'.

        Args:
            s: submited string

        Returns:
            replaced slash string
        """
        s = re.sub('[" "\/\--.]+', '-', s)
        s = re.sub(r':-', ':', s)
        s = re.sub(r'^-|-$', '', s)

        return s


class SiteHelpers(object):
    """Site Helper.

    This helper will support several functions.
    """
    def __init__(self):
        pass

    def strip_html_tags(self, html):
        s = MLStripper()
        s.feed(html)

        return s.get_data()

    def secure_filename(self, name):
        h = ReHelper()
        s = h.r_slash(name)

        return s.lower()

#init function
site_helpers = SiteHelpers()
