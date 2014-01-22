# -*- coding: utf-8 -*-
from config import ThemeConfig

root = ThemeConfig.NAME

templates = dict(
    home="frontend/themes/%s/home.html" % root,
    diary_detail="frontend/themes/%s/diary/detail.html" % root,
    diary_list="frontend/themes/%s/diary/list.html" % root,
    rss="frontend/themes/%s/rss.html" % root
)
