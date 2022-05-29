# -*- coding: utf-8 -*-

from unittest import TestCase

from cachy.stores import NullStore


class NullStoreTestCase(TestCase):
    def test_items_cannot_be_cached(self):
        store = NullStore()
        store.put("foo", "bar", 10)
        self.assertIsNone(store.get("foo"))
