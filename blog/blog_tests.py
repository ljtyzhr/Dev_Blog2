# -*- coding: utf-8 -*-

import unittest
from mongoengine import connect
from mongoengine.connection import get_db

from config import Config
from functions import user_func, cat_func, diary_func, other_func
from utils.helper.helpers import site_helpers


class BlogTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        connect(Config.MONGODB_SETTINGS.get('DB'))
        self.db = get_db()
        self.username = "test_user"
        self.password = "test_password"

    @classmethod
    def tearDownClass(self):
        self.db.drop_collection('user')
        self.db.drop_collection('category')
        self.db.drop_collection('post')

    """TestCase for User functions"""
    def test_generate_user(self):
        user = user_func.generate_user(self.username, self.password)

        self.assertEqual(user.name, self.username)

    def test_get_profile(self):
        user_func.generate_user(self.username, self.password)

        user = user_func.get_profile()

        self.assertEqual(user.name, self.username)

    def test_delete_user(self):
        user_func.generate_user(self.username, self.password)

        user = user_func.delete_user()

        self.assertEqual(None, user)

    """TestCase for Category functions"""
    def test_add_new_category(self):
        cat_name = 'test-category'

        category = cat_func.add_new_category(cat_name=cat_name)

        self.assertEqual(cat_name, category.name)

    def test_add_new_category_with_same_name(self):
        cat_name = 'test-category'

        category = cat_func.add_new_category(cat_name=cat_name)

        self.assertEqual('category name not unique', category)

    def test_get_category_count(self):
        cat_num = cat_func.get_category_count()

        self.assertEqual(1, cat_num)

    def test_get_category_detail(self):
        cat_name = 'test-category'

        category = cat_func.get_category_detail(cat_name=cat_name)

        self.assertEqual(cat_name, category.name)

    """TestCase for SiteHelper functions"""
    def test_strip_html_tags(self):
        html = '<p>Get this pure <span style="">please</span>.</p>'

        pure_content = site_helpers.strip_html_tags(html)

        self.assertEqual('Get this pure please.', pure_content)

    def test_secure_filename(self):
        name1 = 'white space'
        name2 = '../folder'
        name3 = '/abc/cc'
        name4 = 'UPPER NAme'
        name5 = u'/你/好'

        self.assertEqual('white-space', site_helpers.secure_filename(name1))
        self.assertEqual('folder', site_helpers.secure_filename(name2))
        self.assertEqual('abc-cc', site_helpers.secure_filename(name3))
        self.assertEqual('upper-name', site_helpers.secure_filename(name4))
        self.assertEqual(u'你-好', site_helpers.secure_filename(name5))

    """TestCase for Diary functions"""
    def test_edit_diary(self):
        permalink = 'New post'
        title = 'New Post'
        content = '[S](http://s/)'
        categories = ['uncategoried', 'new category']
        tags = ['tag1', 'tag2', 'tags']
        author = user_func.get_profile()
        status = 'Draft'

        diary = diary_func.edit_diary(permalink=permalink, title=title,
                                      content=content, categories=categories,
                                      tags=tags, author=author, status=status)

        self.assertEqual('new-post', diary.permalink)
        self.assertEqual(title, diary.title)
        self.assertEqual(content, diary.content)
        self.assertEqual(categories, diary.categories)
        self.assertEqual(tags, diary.tags)
        self.assertEqual(status, diary.status)
        self.assertEqual(None, diary.publish_time)
        self.assertEqual('<p><a href="http://s/">S</a></p>', diary.html)
        self.assertEqual('S', diary.pure_content)
        self.assertEqual(author, diary.author)

    """TestCase for Other functions"""
    def test_up_img_to_upyun(self):
        collection = 'test_collection'
        data = ''
        filename = 'test.jpg'

        success, url = other_func.up_img_to_upyun(collection, data, filename)

if __name__ == '__main__':
    unittest.main()
