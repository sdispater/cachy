# -*- coding: utf-8 -*-

import hashlib
from .tagged_cache import TaggedCache
from .utils import encode


class RedisTaggedCache(TaggedCache):

    def forever(self, key, value):
        """
        Store an item in the cache indefinitely.

        :param key: The cache key
        :type key: str

        :param value: The value
        :type value: mixed
        """
        namespace = self._tags.get_namespace()

        self._push_forever_keys(namespace, key)

        self._store.forever(
            '%s:%s' % (hashlib.sha1(encode(self._tags.get_namespace())).hexdigest(), key),
            value
        )

    def flush(self):
        """
        Remove all items from the cache.
        """
        self._delete_forever_keys()

        super(RedisTaggedCache, self).flush()

    def _push_forever_keys(self, namespace, key):
        """
        Store a copy of the full key for each namespace segment.

        :type namespace: str
        :type key: str
        """
        full_key = '%s%s:%s' % (self.get_prefix(),
                                hashlib.sha1(encode(self._tags.get_namespace())).hexdigest(),
                                key)

        for segment in namespace.split('|'):
            self._store.connection().lpush(self._forever_key(segment), full_key)

    def _delete_forever_keys(self):
        """
        Delete all of the items that were stored forever.
        """
        for segment in self._tags.get_namespace().split('|'):
            segment = self._forever_key(segment)
            self._delete_forever_values(segment)

            self._store.connection().delete(segment)

    def _delete_forever_values(self, forever_key):
        """
        Delete all of the keys that have been stored forever.

        :type forever_key: str
        """
        forever = self._store.connection().lrange(forever_key, 0, -1)

        if len(forever) > 0:
            self._store.connection().delete(*forever)

    def _forever_key(self, segment):
        """
        Get the forever reference key for the segment.

        :type segment: str

        :rtype: str
        """
        return '%s%s:forever' % (self.get_prefix(), segment)
