import unittest
import os
from flask_testing import TestCase
from flask import request, url_for

from app.controllers import app
from app.models.model import *


class TestApp(TestCase):

    def create_app(self):
        test_app = app
        test_app.config['WTF_CSRF_ENABLED'] = False
        test_app.config['TESTING'] = True
        test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../test.db'
        return test_app

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
