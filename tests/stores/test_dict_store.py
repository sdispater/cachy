# -*- coding: utf-8 -*-

from unittest import TestCase

from flexmock import flexmock, flexmock_teardown

from cachy.stores import DictStore


class DictStoreTestCase(TestCase):
    def tearDown(self):
        flexmock_teardown()

    def test_items_can_be_set_and_retrieved(self):
        store = DictStore()
        store.put("foo", "bar", 10)

        self.assertEqual("bar", store.get("foo"))

    def test_store_item_forever_properly_stores_in_dict(self):
        mock = flexmock(DictStore())
        mock.should_receive("put").once().with_args("foo", "bar", 0)
        mock.forever("foo", "bar")

    def test_values_can_be_incremented(self):
        store = DictStore()
        store.put("foo", 1, 10)
        store.increment("foo")

        self.assertEqual(2, store.get("foo"))

    def test_values_can_be_decremented(self):
        store = DictStore()
        store.put("foo", 1, 10)
        store.decrement("foo")

        self.assertEqual(0, store.get("foo"))

    def test_values_can_be_removed(self):
        store = DictStore()
        store.put("foo", "bar", 10)
        store.forget("foo")

        self.assertIsNone(store.get("foo"))

    def test_items_can_be_flushed(self):
        store = DictStore()
        store.put("foo", "bar", 10)
        store.put("baz", "boom", 10)
        store.flush()

        self.assertIsNone(store.get("foo"))
        self.assertIsNone(store.get("baz"))

    def test_cache_key(self):
        store = DictStore()

        self.assertEqual("", store.get_prefix())
