# -*- coding: utf-8 -*-
import unittest2 as unittest
from tests import MyModel
from snippets import snippet, purge

class TestModel(unittest.TestCase):

    def setUp(self):
        self.m = MyModel(id=1, name='awesome title')

    def test_property(self):
        m = self.m
        self.assertIn('<h1>awesome title</h1>', m.h1)

    def test_tag(self):
        m = self.m
        self.assertIn('<h1><a href=', m.a_tag)

    def test_custom_template(self):
        m = self.m
        self.assertIn('<h1><a href=', m.custom_template)

    def test_cached_tag(self):
        m = self.m
        self.assertIn('<h1><a href=', m.a_cached_tag)
        cached = m.a_cached_tag
        m.name = 'ugly title'
        self.assert_(m.a_cached_tag == cached)
        purge(m)
        self.assertIn('ugly title', m.a_cached_tag)

