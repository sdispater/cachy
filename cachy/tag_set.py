# -*- coding: utf-8 -*-

import uuid


class TagSet(object):

    def __init__(self, store, names=None):
        """
        :param store: The cache store implementation
        :type store: cachy.contracts.store.Store

        :param names: The tags names
        :type names: list or tuple
        """
        self._store = store
        self._names = names or []

    def reset(self):
        """
        Reset all tags in the set.
        """
        list(map(self.reset_tag, self._names))

    def tag_id(self, name):
        """
        Get the unique tag identifier for a given tag.

        :param name: The tag
        :type name: str

        :rtype: str
        """
        return self._store.get(self.tag_key(name)) or self.reset_tag(name)

    def _tag_ids(self):
        """
        Get a list of tag identifiers for all of the tags in the set.

        :rtype: list
        """
        return list(map(self.tag_id, self._names))

    def get_namespace(self):
        """
        Get a unique namespace that changes when any of the tags are flushed.

        :rtype: str
        """
        return '|'.join(self._tag_ids())

    def reset_tag(self, name):
        """
        Reset the tag and return the new tag identifier.

        :param name: The tag
        :type name: str

        :rtype: str
        """
        id_ = str(uuid.uuid4()).replace('-', '')

        self._store.forever(self.tag_key(name), id_)

        return id_

    def tag_key(self, name):
        """
        Get the tag identifier key for a given tag.

        :param name: The tag
        :type name: str

        :rtype: str
        """
        return 'tag:%s:key' % name
