# -*- coding: utf-8 -*-

from unittest import TestCase

from cachy.stores import MemcachedStore


class RedisStoreTestCase(TestCase):
    def setUp(self):
        self.store = MemcachedStore(["127.0.0.1:11211"], "prefix:")

        super(RedisStoreTestCase, self).setUp()

    def tearDown(self):
        self.store._memcache.flush_all()

    def test_get_returns_null_when_not_found(self):
        self.assertIsNone(self.store.get("foo"))

    def test_value_is_returned(self):
        mc = self.get_memcached()
        mc.set("prefix:foo", "bar")

        self.assertEqual("bar", self.store.get("foo"))

    def test_value_is_returned_for_numerics(self):
        mc = self.get_memcached()
        mc.set("prefix:foo", 1)

        self.assertEqual(1, self.store.get("foo"))

    def test_put_value_into_memcache(self):
        mc = self.get_memcached()
        self.store.put("foo", "bar", 60)

        self.assertEqual("bar", mc.get("prefix:foo"))

    def test_put_numeric_value(self):
        mc = self.get_memcached()
        self.store.put("foo", 1, 60)

        self.assertEqual(1, mc.get("prefix:foo"))

    def test_increment(self):
        mc = self.get_memcached()
        mc.set("prefix:foo", 1, 60)

        self.store.increment("foo", 2)
        self.assertEqual(3, mc.get("prefix:foo"))

    def test_decrement(self):
        mc = self.get_memcached()
        mc.set("prefix:foo", 3, 60)

        self.store.decrement("foo", 2)
        self.assertEqual(1, mc.get("prefix:foo"))

    def test_forever(self):
        mc = self.get_memcached()

        self.store.forever("foo", "bar")

        self.assertEqual("bar", mc.get("prefix:foo"))

    def test_forget(self):
        mc = self.get_memcached()
        mc.set("prefix:foo", "bar")

        self.store.forget("foo")

        self.assertIsNone(mc.get("prefix:foo"))

    def get_memcached(self):
        return self.store._memcache
