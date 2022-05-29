# -*- coding: utf-8 -*-

import datetime
from unittest import TestCase

from flexmock import flexmock, flexmock_teardown

from cachy import Repository
from cachy.contracts.store import Store


class RepositoryTestCase(TestCase):
    def tearDown(self):
        flexmock_teardown()

    def test_get_returns_value_from_cache(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").once().with_args("foo").and_return("bar")

        self.assertEqual("bar", repo.get("foo"))

    def test_default_value_is_returned(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").and_return(None)

        self.assertEqual("bar", repo.get("foo", "bar"))
        self.assertEqual("baz", repo.get("foo", lambda: "baz"))

    def test_set_default_cache_time(self):
        repo = self._get_repository()
        repo.set_default_cache_time(10)

        self.assertEqual(10, repo.get_default_cache_time())

    def test_has_method(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").with_args("foo").and_return(None)
        repo.get_store().should_receive("get").with_args("bar").and_return("baz")

        self.assertFalse(repo.has("foo"))
        self.assertTrue(repo.has("bar"))

    def test_pull(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").with_args("foo").and_return("bar")
        repo.get_store().should_receive("forget").with_args("foo")

        self.assertEqual("bar", repo.get("foo"))

    def test_put(self):
        repo = self._get_repository()
        repo.get_store().should_receive("put").with_args("foo", "bar", 10)

        repo.put("foo", "bar", 10)

    def test_put_supports_datetime_as_minutes(self):
        repo = self._get_repository()
        repo.get_store().should_receive("put").with_args("foo", "bar", 60)

        repo.put("foo", "bar", datetime.datetime.now() + datetime.timedelta(hours=1))

    def test_put_with_minutes_to_zero_doesnt_store(self):
        repo = self._get_repository()
        repo.get_store().should_receive("put").never()

        repo.put("foo", "bar", datetime.datetime.now() - datetime.timedelta(hours=1))

    def test_add(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").once().with_args("foo").and_return(None)
        repo.get_store().should_receive("get").once().with_args("bar").and_return("baz")
        repo.get_store().should_receive("put").once().with_args("foo", "bar", 10)
        repo.get_store().should_receive("put").never().with_args("bar", "baz", 10)

        self.assertTrue(repo.add("foo", "bar", 10))
        self.assertFalse(repo.add("bar", "baz", 10))

    def test_forever(self):
        repo = self._get_repository()
        repo.get_store().should_receive("forever").once().with_args("foo", "bar")

        repo.forever("foo", "bar")

    def test_remember_calls_put_and_returns_default(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").and_return(None)
        repo.get_store().should_receive("put").once().with_args("foo", "bar", 10)
        result = repo.remember("foo", 10, lambda: "bar")

        self.assertEqual("bar", result)

    def test_remember_forever_calls_forever_and_returns_default(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").and_return(None)
        repo.get_store().should_receive("forever").once().with_args("foo", "bar")
        result = repo.remember_forever("foo", lambda: "bar")

        self.assertEqual("bar", result)

    def test_repository_can_serve_as_a_decorator(self):
        repo = self._get_repository()
        repo.get_store().should_receive("get").and_return(None, 6, 6).one_by_one()
        repo.get_store().should_receive("put").once()
        calls = []

        @repo
        def test(i, m=3):
            calls.append(i)

            return i * 3

        test(2)
        test(2)
        test(2)

        self.assertEqual(1, len(calls))

    def test_repository_can_serve_as_a_decorator_with_key_and_minutes(self):
        repo = flexmock(self._get_repository())
        repo.should_receive("_get_key").with_args("my_key", (2,), {"m": 4}).and_return(
            "foo"
        )
        repo.get_store().should_receive("get").and_return(None, 6, 6).one_by_one()
        repo.get_store().should_receive("put").once().with_args("foo", 6, 35)
        calls = []

        @repo(key="my_key", minutes=35)
        def test(i, m=3):
            calls.append(i)

            return i * 3

        test(2, m=4)
        test(2, m=4)
        test(2, m=4)

        self.assertEqual(1, len(calls))

    def _get_repository(self):
        repo = Repository(flexmock(Store()))

        return repo
