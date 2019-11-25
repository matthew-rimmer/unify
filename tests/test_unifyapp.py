#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from unify.unifyapp import UnifyApp


class TestUnifyApp(unittest.TestCase):
    """TestCase for UnifyApp.
    """
    def setUp(self):
        self.app = UnifyApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'unify')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
