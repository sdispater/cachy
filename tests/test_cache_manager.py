# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase
from flexmock import flexmock, flexmock_teardown

from cachy import CacheManager, Repository
from cachy.stores import DictStore, FileStore
from cachy.contracts.store import Store


class RepositoryTestCase(TestCase):

    def tearDown(self):
        flexmock_teardown()

    def test_store_get_the_correct_store(self):
        cache = CacheManager({
            'default': 'dict',
            'stores': {
                'dict': {
                    'driver': 'dict'
                },
                'file': {
                    'driver': 'file',
                    'path': os.path.join(tempfile.gettempdir(), 'cachy')
                }
            }
        })

        self.assertIsInstance(cache.store().get_store(), DictStore)
        self.assertIsInstance(cache.store('dict').get_store(), DictStore)
        self.assertIsInstance(cache.store('file').get_store(), FileStore)

    def test_set_default_driver_changes_driver(self):
        cache = CacheManager({
            'default': 'dict',
            'stores': {
                'dict': {
                    'driver': 'dict'
                },
                'file': {
                    'driver': 'file',
                    'path': os.path.join(tempfile.gettempdir(), 'cachy')
                }
            }
        })

        self.assertIsInstance(cache.store().get_store(), DictStore)
        cache.set_default_driver('file')
        self.assertIsInstance(cache.store().get_store(), FileStore)

    def test_extend_accepts_a_callable_returning_a_store(self):
        cache = CacheManager({
            'default': 'my-driver',
            'stores': {
                'my-driver': {
                    'driver': 'my-driver'
                }
            }
        })

        cache.extend('my-driver', lambda config: CustomStore())

        self.assertIsInstance(cache.store().get_store(), CustomStore)

    def test_extend_accepts_a_callable_returning_a_repository(self):
        cache = CacheManager({
            'default': 'my-driver',
            'stores': {
                'my-driver': {
                    'driver': 'my-driver'
                }
            }
        })

        cache.extend('my-driver', lambda config: Repository(CustomStore()))

        self.assertIsInstance(cache.store().get_store(), CustomStore)

    def test_extend_accepts_a_store_class(self):
        cache = CacheManager({
            'default': 'my-driver',
            'stores': {
                'my-driver': {
                    'driver': 'my-driver'
                }
            }
        })

        cache.extend('my-driver', CustomStore)

        self.assertIsInstance(cache.store().get_store(), CustomStore)

    def test_default_store_with_one_store(self):
        manager = CacheManager({
            'stores': {
                'dict': {
                    'driver': 'dict'
                }
            }
        })

        self.assertEqual('dict', manager.get_default_driver())


class CustomStore(Store):

    def __init__(self, config=None):
        pass
