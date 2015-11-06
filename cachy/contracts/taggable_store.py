# -*- coding: utf-8 -*-

from .store import Store
from ..tagged_cache import TaggedCache
from ..tag_set import TagSet


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
