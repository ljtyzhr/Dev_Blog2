# -*- coding: utf-8 -*-
from model.models import User, Diary, Category, StaticPage


class Functions(object):

    """User functions.
    Return author profile
    """
    def get_profile(self):
        return User.objects.first()

    """Diary functions.
    Return diary objects
    """
    def get_all_diaries(self, order):
        return Diary.objects.order_by(order)

    def get_diary(self, diary_id):
        return Diary.objects(pk=diary_id).first()

    def get_first_diary(self):
        return Diary.objects.order_by('-publish_time').first()

    def get_last_diary(self):
        return Diary.objects.order_by('publish_time').first()

    """Category functions.
    Return category objects
    """
    def get_all_categories(self, order):
        return Category.objects.order_by(order)

    """Page functions.
    Return page objects
    """
    def get_all_pages(self, order):
        return StaticPage.objects.order_by(order)
