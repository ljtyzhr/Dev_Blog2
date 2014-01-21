# -*- coding: utf-8 -*-

import unittest

import runserver


class BlogTestCase(unittest.TestCase):

    def setUp(self):
        self.app = runserver.app.test_client()

    def login(self, username, password):
        return self.app.post('/admin/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/admin/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Powered By Tornado and MongoDB' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        assert 'welcome' in rv.data
        rv = self.logout()
        assert 'Please log in' in rv.data
        rv = self.login('adminx', 'default')
        assert 'type your password and log' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'type your password and log' in rv.data


if __name__ == '__main__':
    unittest.main()
