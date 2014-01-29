# -*- coding: utf-8 -*-

import unittest
from mongoengine import connect
from mongoengine.connection import get_db

from config import Config
from functions import user_func, cat_func


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

if __name__ == '__main__':
    unittest.main()
