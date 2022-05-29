# -*- coding: utf-8 -*-


class Factory:
    """
    Represent a cahce factory.
    """

    def store(self, name=None):
        """
        Get a cache store instance by name.

        :param name: The cache store name
        :type name: str

        :rtype: mixed
        """
        raise NotImplementedError()
