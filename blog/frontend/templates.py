# -*- coding: utf-8 -*-
from config import ThemeConfig

templates = dict(
    home="frontend/themes/%s/home.html" % ThemeConfig.NAME,
    diary_detail="frontend/themes/%s/diary/detail.html" % ThemeConfig.NAME
)
