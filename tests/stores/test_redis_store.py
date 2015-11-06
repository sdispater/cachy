# -*- coding: utf-8 -*-

import math
from unittest import TestCase
from flexmock import flexmock, flexmock_teardown
from fakeredis import FakeStrictRedis
from cachy.stores import RedisStore


class RedisStoreTestCase(TestCase):

    def setUp(self):
        self.redis = FakeStrictRedis()

        super(RedisStoreTestCase, self).setUp()

    def tearDown(self):
        flexmock_teardown()
        self.redis.flushdb()

    def test_get_returns_null_when_not_found(self):
        store = self.get_store()

        self.assertIsNone(store.get('foo'))

    def test_redis_value_is_returned(self):
        store = self.get_store()
        self.redis.set('prefix:foo', store.serialize('bar'))

        self.assertEqual('bar', store.get('foo'))

    def test_redis_value_is_returned_for_numerics(self):
        store = self.get_store()
        self.redis.set('prefix:foo', store.serialize(1))

        self.assertEqual(1, store.get('foo'))

    def test_put_value_into_redis(self):
        store = self.get_store()
        store.put('foo', 'bar', 60)

        self.assertEqual(store.serialize('bar'), self.redis.get('prefix:foo'))
        self.assertEqual(60., round(math.ceil(float(self.redis.ttl('prefix:foo')) / 60)))

    def test_put_numeric_value_into_redis(self):
        store = self.get_store()
        store.put('foo', 1, 60)

        self.assertEqual(store.serialize(1), self.redis.get('prefix:foo'))
        self.assertEqual(60., round(math.ceil(float(self.redis.ttl('prefix:foo')) / 60)))

    def test_increment(self):
        store = self.get_store()
        self.redis.set('prefix:foo', 1)

        store.increment('foo', 2)
        self.assertEqual(3, int(self.redis.get('prefix:foo')))

    def test_decrement(self):
        store = self.get_store()
        self.redis.set('prefix:foo', 3)

        store.decrement('foo', 2)
        self.assertEqual(1, int(self.redis.get('prefix:foo')))

    def test_forever(self):
        store = self.get_store()

        store.forever('foo', 'bar')

        self.assertEqual(store.serialize('bar'), self.redis.get('prefix:foo'))
        self.assertIsNone(self.redis.ttl('prefix:foo'))

    def test_forget(self):
        store = self.get_store()
        self.redis.set('prefix:foo', 'bar')

        store.forget('foo')

        self.assertFalse(self.redis.exists('prefix:foo'))

    def get_store(self):
        return RedisStore(prefix='prefix:', redis_class=FakeStrictRedis)
