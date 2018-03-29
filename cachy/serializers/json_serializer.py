# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json

from cachy.utils import decode

from .serializer import Serializer


class JsonSerializer(Serializer):
    """
    Serializer that uses JSON representations.
    """

    def serialize(self, data):
        """
        Serialize data.

        :param data: The data to serialize
        :type data: mixed

        :rtype: str
        """
        return json.dumps(data)

    def unserialize(self, data):
        """
        Unserialize data.

        :param data: The data to unserialize
        :type data: mixed

        :rtype: str
        """
        return json.loads(decode(data))
