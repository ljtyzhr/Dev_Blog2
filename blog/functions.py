# -*- coding: utf-8 -*-
import datetime
import PyRSS2Gen
from werkzeug.security import generate_password_hash
from mongoengine.errors import NotUniqueError

from config import Config
from model.models import User, Diary, Category, Page


class UserFunctions(object):
    """User functions.
    Return author profile
    """
    def get_profile(self):
        """Return User object."""
        return User.objects.first()

    def generate_user(self, username, password):
        """Generate User"""
        user = User(name=username)
        user.password = generate_password_hash(password=password)
        return user.save()

    def delete_user(self):
        """Delete User"""
        return User.objects().first().delete()


class DiaryFunctions(object):

    def get_all_diaries(self, order='-publish_time'):
        """Return Total diaries objects."""
        return Diary.objects.order_by(order)

    def get_diary(self, diary_id):
        """Diary detail.
        Only return diary detail by diary_id.

        Args:
            diary_id: objectID

        Return:
            diary: diary object
        """
        return Diary.objects(pk=diary_id).first()

    def get_diary_width_navi(self, diary_id):
        """Diary Detail Width page navi boolean.
        get diary detail and if there should be prev or next page.

        Args:
            diary_id: objectID

        Return:
            diary: diary object
            prev: boolean, can be used as 'prev' logic
            next: boolean, can be used as 'next' logic
        """
        prev = next = True
        diary = self.get_diary(diary_id)
        if diary == self.get_first_diary():
            next = False
        if diary == self.get_last_diary():
            prev = False

        return prev, next, diary

    def get_first_diary(self):
        """Return First Diary object."""
        return Diary.objects.order_by('-publish_time').first()

    def get_last_diary(self):
        """Return Last Diary object."""
        return Diary.objects.order_by('publish_time').first()

    def get_prev_diary(self, pub_time):
        """Return Previous Diary object."""
        return Diary.objects(publish_time__lt=pub_time
                             ).order_by('-publish_time').first()

    def get_next_diary(self, pub_time):
        """Return Next Diary object."""
        return Diary.objects(publish_time__gt=pub_time
                             ).order_by('-publish_time').first()

    def get_next_or_prev_diary(self, prev_or_next, diary_id):
        """Diary route prev or next function.
        Use publish_time to determin what`s the routed diary.

        Args:
            prev_or_next: string 'prev' or 'next'
            diary_id: objectID

        Return:
            next_diary: routed diary object
        """
        diary = self.get_diary(diary_id)

        if prev_or_next == 'prev':
            next_diary = self.get_prev_diary(diary.publish_time)
        else:
            next_diary = self.get_next_diary(diary.publish_time)

        return next_diary

    def get_diary_count(self):
        """Return Diaries total number."""
        return Diary.objects.count()

    def get_diary_list(self, start=0, end=10, order='-publish_time'):
        """Diary list.
        default query 10 diaries and return if there should be next or prev
        page.

        Args:
            start: num defalut 0
            end: num defalut 10
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            diaries: diaries list
        """
        size = end - start
        prev = next = False
        diaries = Diary.objects.order_by(order)[start:end + 1]
        if len(diaries) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, diaries[start:end]


class CategoryFunctions(object):
    """Category functions.
    Return category objects
    """
    def get_all_categories(self, order='-publish_time'):
        """Return Total Categories objects."""
        return Category.objects.order_by(order)

    def get_diary_list(self, cat_name, start=0, end=10, order='-publish_time'):
        """Category Diary list.
        default query 10 diaries and return if there should be next or prev
        page.

        Args:
            start: num defalut 0
            end: num defalut 10
            order: str defalut '-publish_time'

        Return:
            next: boolean
            prev: boolean
            diaries: diaries list
        """
        size = end - start
        prev = next = False
        diaries = Diary.objects(category=cat_name).order_by(order)[start:
                                                                   end + 1]
        if len(diaries) - size > 0:
            next = True
        if start != 0:
            prev = True

        return prev, next, diaries[start:end]

    def get_category_count(self):
        """Return Categories total number."""
        return Category.objects.count()

    def add_new_category(self, cat_name):
        """Category add new.
        Will check if the cat_name is unique, otherwise will return an error.

        Args:
            cat_name: string category name.

        Return:
            None
        """
        try:
            return Category(name=cat_name).save()
        except NotUniqueError:
            return 'category name not unique'

    def get_category_detail(self, cat_name):
        """Category detail.
        will return category detail by category name.

        Args:
            cat_name: string category name.

        Return:
            category: category object
        """
        return Category.objects(name=cat_name).first()


class PageFunctions(object):
    """Page functions.
    Return page objects
    """
    def get_all_pages(self, order='-publish_time'):
        return Page.objects.order_by(order)

    def get_page(self, page_url):
        return Page.objects(url=page_url).first()


class OtherFunctions(object):

    def get_rss(self, size):
        """ RSS2 Support.

            support xml for RSSItem with sized diaries.

        Args:
            none
        Return:
            rss: xml
        """
        articles = Diary.objects.order_by('-publish_time')[:size]
        items = []
        for article in articles:
            content = article.html

            url = Config.SITE_URL + '/diary/' + str(article.pk) + '/' + \
                article.title
            items.append(PyRSS2Gen.RSSItem(
                title=article.title,
                link=url,
                description=content,
                guid=PyRSS2Gen.Guid(url),
                pubDate=article.publish_time,
            ))
        rss = PyRSS2Gen.RSS2(
            title=Config.MAIN_TITLE,
            link=Config.SITE_URL,
            description=Config.DESCRIPTION,
            lastBuildDate=datetime.datetime.now(),
            items=items
        ).to_xml('utf-8')
        return rss

# init functions
user_func = UserFunctions()
diary_func = DiaryFunctions()
cat_func = CategoryFunctions()
page_func = PageFunctions()
other_func = OtherFunctions()
