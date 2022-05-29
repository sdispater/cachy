# -*- coding: utf-8 -*-

import builtins
import glob
import hashlib
import os
import shutil
import tempfile
from unittest import TestCase

from flexmock import flexmock, flexmock_teardown

from cachy.serializers import JsonSerializer
from cachy.stores import FileStore
from cachy.utils import encode


class DictStoreTestCase(TestCase):
    def setUp(self):
        self._dir = os.path.join(tempfile.gettempdir(), "cachy")

    def tearDown(self):
        for e in glob.glob(os.path.join(self._dir, "*")):
            if os.path.isdir(e):
                shutil.rmtree(e)

        flexmock_teardown()

    def test_none_is_returned_if_file_doesnt_exist(self):
        mock = flexmock(os.path)
        mock.should_receive("exists").once().and_return(False)

        store = FileStore(tempfile.gettempdir())

        self.assertIsNone(store.get("foo"))

    def test_put_creates_missing_directories(self):
        store = flexmock(FileStore(self._dir))
        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)
        store.should_receive("_create_cache_directory").once().with_args(full_path)
        mock = flexmock(builtins)
        handler = flexmock()
        mock.should_receive("open").once().with_args(full_path, "wb").and_return(
            handler
        )
        handler.should_receive("write").once()

        store.put("foo", "0000000000", 0)

    def test_expired_items_return_none(self):
        store = flexmock(FileStore(self._dir))
        contents = b"0000000000" + store.serialize("bar")

        flexmock(os.path).should_receive("exists").once().and_return(True)

        mock = flexmock(builtins)
        handler = flexmock()

        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)

        mock.should_receive("open").once().with_args(full_path, "rb").and_return(
            handler
        )
        handler.should_receive("read").once().and_return(contents)

        store.should_receive("forget").once().with_args("foo")

        store.get("foo")

    def test_store_items_properly_store_values(self):
        store = flexmock(FileStore(self._dir))

        contents = b"1111111111" + store.serialize("bar")

        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)

        store.should_receive("_expiration").with_args(10).and_return(1111111111)

        mock = flexmock(builtins)
        handler = flexmock()
        mock.should_receive("open").once().with_args(full_path, "wb").and_return(
            handler
        )
        handler.should_receive("write").once().with_args(contents)

        store.put("foo", "bar", 10)

    def test_forever_store_values_with_high_timestamp(self):
        store = flexmock(FileStore(self._dir))

        contents = b"9999999999" + store.serialize("bar")

        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)

        mock = flexmock(builtins)
        handler = flexmock()
        mock.should_receive("open").once().with_args(full_path, "wb").and_return(
            handler
        )
        handler.should_receive("write").once().with_args(contents)

        store.forever("foo", "bar")

    def test_forget_with_missing_file(self):
        store = FileStore(self._dir)

        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)

        mock = flexmock(os.path)
        mock.should_receive("exists").once().with_args(full_path).and_return(False)

        self.assertFalse(store.forget("foo"))

    def test_forget_removes_file(self):
        store = FileStore(self._dir)

        sha = hashlib.sha256(encode("foo")).hexdigest()
        full_dir = os.path.join(
            self._dir,
            sha[0:2],
            sha[2:4],
            sha[4:6],
            sha[6:8],
            sha[8:10],
            sha[10:12],
            sha[12:14],
            sha[14:16],
        )
        full_path = os.path.join(full_dir, sha)

        mock = flexmock(os.path)
        mock.should_receive("exists").once().with_args(full_path).and_return(True)
        flexmock(os).should_receive("remove").once().with_args(full_path)

        self.assertTrue(store.forget("foo"))

    def test_get_with_json_serializer(self):
        store = FileStore(self._dir)
        store.set_serializer(JsonSerializer())
        store.forever("foo", {"foo": "bar"})

        result = store.get("foo")
        assert result == {"foo": "bar"}

    def test_set_hash_type(self):
        store = FileStore(self._dir, hash_type="md5")

        store.put("foo", "bar", 10)
        md5 = hashlib.md5(encode("foo")).hexdigest()

        full_dir = os.path.join(self._dir, md5[0:2], md5[2:4])

        assert os.path.exists(full_dir)
