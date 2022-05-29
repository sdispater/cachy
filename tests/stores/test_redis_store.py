# -*- coding: utf-8 -*-

import math
from unittest import TestCase

from fakeredis import FakeServer, FakeStrictRedis
from flexmock import flexmock_teardown

from cachy.stores import RedisStore


class RedisStoreTestCase(TestCase):
    def setUp(self):
        server = FakeServer()
        server.connected = True
        self.store = RedisStore(
            prefix="prefix:", redis_class=FakeStrictRedis, server=server
        )
        self.redis = FakeStrictRedis(server=server)

        super(RedisStoreTestCase, self).setUp()

    def tearDown(self):
        flexmock_teardown()
        self.redis.flushdb()

    def test_get_returns_null_when_not_found(self):
        self.assertIsNone(self.store.get("foo"))

    def test_redis_value_is_returned(self):
        self.redis.set("prefix:foo", self.store.serialize("bar"))

        self.assertEqual("bar", self.store.get("foo"))

    def test_redis_value_is_returned_for_numerics(self):
        self.redis.set("prefix:foo", self.store.serialize(1))

        self.assertEqual(1, self.store.get("foo"))

    def test_put_value_into_redis(self):
        self.store.put("foo", "bar", 60)

        self.assertEqual(self.store.serialize("bar"), self.redis.get("prefix:foo"))
        self.assertEqual(
            60.0, round(math.ceil(float(self.redis.ttl("prefix:foo")) / 60))
        )

    def test_put_numeric_value_into_redis(self):
        self.store.put("foo", 1, 60)

        self.assertEqual(self.store.serialize(1), self.redis.get("prefix:foo"))
        self.assertEqual(
            60.0, round(math.ceil(float(self.redis.ttl("prefix:foo")) / 60))
        )

    def test_increment(self):
        self.redis.set("prefix:foo", 1)

        self.store.increment("foo", 2)
        self.assertEqual(3, int(self.redis.get("prefix:foo")))

    def test_decrement(self):
        self.redis.set("prefix:foo", 3)

        self.store.decrement("foo", 2)
        self.assertEqual(1, int(self.redis.get("prefix:foo")))

    def test_forever(self):
        self.store.forever("foo", "bar")

        self.assertEqual(self.store.serialize("bar"), self.redis.get("prefix:foo"))
        assert self.redis.ttl("prefix:foo") == -1

    def test_forget(self):
        self.redis.set("prefix:foo", "bar")

        self.store.forget("foo")

        self.assertFalse(self.redis.exists("prefix:foo"))
