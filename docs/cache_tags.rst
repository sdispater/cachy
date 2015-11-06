.. _CacheTags:

Cache Tags
##########

.. note::

    Cache tags are not supported when using the ``file`` or ``database`` cache drivers.
    Furthermore, when using multiple tags with caches that are stored "forever",
    performance will be best with a driver such as ``memcached``, which automatically purges stale records.


Storing Tagged Cache Items
==========================

Cache tags allow you to tag related items in the cache and then flush all cached values that assigned a given tag.
You may access a tagged cache by passing in an ordered array of tag names.
For example, let's access a tagged cache and ``put`` value in the cache:

.. code-block:: python

    cache.tags('people', 'artists').put('John', john, minutes)
    cache.tags('people', 'authors').put('Anne', anne, minutes)

However, you are not limited to the ``put`` method. You can use any cache storage method
while working with tags.


Accessing Tagged Cache Items
============================

To retrieve a tagged cache item, pass the same ordered list of tags to the ``tags`` method:

.. code-block:: python

    john = cache.tags('people', 'artists').get('John')
    anne = cache.tags('people', 'authors').get('Anne')

You can flush all items that are assigned a tag or list of tags.
For example, this statement would remove all caches tagged with either ``people``, ``authors`, or both.
So, both ``Anne`` and ``John`` would be removed from the cache:

.. code-block:: python

    cache.tags('people', 'authors').flush()

In contrast, this statement would remove only caches tagged with ``authors``, so ``Anne`` would be removed, but not ``John``.

.. code-block:: python

    cache.tags('authors').flush()
