# -*- coding: utf-8 -*-

from ..tag_set import TagSet
from ..tagged_cache import TaggedCache
from .store import Store


class TaggableStore(Store):
    def tags(self, *names):
        """
        Begin executing a new tags operation.

        :param names: The tags
        :type names: tuple

        :rtype: cachy.tagged_cache.TaggedCache
        """
        if len(names) == 1 and isinstance(names[0], list):
            names = names[0]

        return TaggedCache(self, TagSet(self, names))
