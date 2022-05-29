# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime, timedelta
from unittest import TestCase

from fakeredis import FakeStrictRedis
from flexmock import flexmock, flexmock_teardown

from cachy.redis_tagged_cache import RedisTaggedCache
from cachy.stores import DictStore, RedisStore
from cachy.tag_set import TagSet


class TaggedCacheTestCase(TestCase):
    def tearDown(self):
        flexmock_teardown()

    def test_tags_can_be_flushed(self):
        store = DictStore()

        store.tags("bop").put("foo", "bar", 10)
        store.tags("zap").put("baz", "boom", 10)
        store.tags("bop").flush()

        self.assertIsNone(store.tags("bop").get("foo"))
        self.assertEqual("boom", store.tags("zap").get("baz"))

    def test_cache_can_be_saved_with_multiple_tags(self):
        store = DictStore()

        tags = ["bop", "zap"]
        store.tags(*tags).put("foo", "bar", 10)
        self.assertEqual("bar", store.tags(tags).get("foo"))

    def test_cache_can_be_set_with_datetime(self):
        store = DictStore()
        duration = datetime.now() + timedelta(minutes=10)

        store.tags("bop").put("foo", "bar", duration)

        self.assertEqual("bar", store.tags("bop").get("foo"))

    def test_cache_saved_with_multiple_tags_can_be_flushed(self):
        store = DictStore()

        tags = ["bop", "zap"]
        store.tags(*tags).put("foo", "bar", 10)
        tags2 = ["bam", "pow"]
        store.tags(*tags2).put("foo", "bar", 10)
        store.tags("zap").flush()

        self.assertIsNone(store.tags(tags).get("foo"))
        self.assertEqual("bar", store.tags(tags2).get("foo"))

    def test_tags_cache_forever(self):
        store = DictStore()

        tags = ["bop", "zap"]
        store.tags(*tags).forever("foo", "bar")

        self.assertEqual("bar", store.tags(tags).get("foo"))

    def test_redis_cache_tags_push_forever_keys_correctly(self):
        store = flexmock(RedisStore(redis_class=FakeStrictRedis))
        tag_set = flexmock(TagSet(store, ["foo", "bar"]))

        tag_set.should_receive("get_namespace").and_return("foo|bar")
        redis = RedisTaggedCache(store, tag_set)

        store.should_receive("get_prefix").and_return("prefix:")
        conn = flexmock()
        store.should_receive("connection").and_return(conn)
        conn.should_receive("lpush").once().with_args(
            "prefix:foo:forever",
            "prefix:%s:key1" % hashlib.sha1(b"foo|bar").hexdigest(),
        )
        conn.should_receive("lpush").once().with_args(
            "prefix:bar:forever",
            "prefix:%s:key1" % hashlib.sha1(b"foo|bar").hexdigest(),
        )

        store.should_receive("forever").with_args(
            hashlib.sha1(b"foo|bar").hexdigest() + ":key1", "key1:value"
        )

        redis.forever("key1", "key1:value")

    def test_redis_cache_forever_tags_can_be_flushed(self):
        store = flexmock(RedisStore(redis_class=FakeStrictRedis))
        tag_set = flexmock(TagSet(store, ["foo", "bar"]))

        tag_set.should_receive("get_namespace").and_return("foo|bar")
        redis = RedisTaggedCache(store, tag_set)

        store.should_receive("get_prefix").and_return("prefix:")
        conn = flexmock()
        store.should_receive("connection").and_return(conn)

        conn.should_receive("lrange").once().with_args(
            "prefix:foo:forever", 0, -1
        ).and_return(["key1", "key2"])
        conn.should_receive("lrange").once().with_args(
            "prefix:bar:forever", 0, -1
        ).and_return(["key3"])

        conn.should_receive("delete").once().with_args("key1", "key2")
        conn.should_receive("delete").once().with_args("key3")
        conn.should_receive("delete").once().with_args("prefix:foo:forever")
        conn.should_receive("delete").once().with_args("prefix:bar:forever")

        tag_set.should_receive("reset").once()

        redis.flush()
