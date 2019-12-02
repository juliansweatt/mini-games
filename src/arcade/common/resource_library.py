#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

class ResourceLibrary():
    """General safe resource library which instantiates a new copy of any requested resource.

    """
    def __init__(self, resource_dictionary:dict):
        """Create a new resource library from a dictionary.

        :param dict resource_dictionary: Dictionary of resource to build the library from.
        :return Newly instantiated resource library.
        :rtype: ResourceLibrary
        """
        self.__d__:dict = resource_dictionary

    def get(self, requested_resource:str) -> Union[object, bool]:
        """Get a copy of the resource, if it exists.

        :param str requested_resource: Name/key of the resource.
        :return A copy of the requested resource, or False if it does not exist.
        """
        return self.__d__.get(requested_resource).copy() or False

    def set_resource(self, resource_key:str, resource_value:object) -> None:
        """Add a new resource to the library.

        :param str resource_key: Key of the resource.
        :param object resource_value: Value of the resource.
        :rtype: None
        """
        self.__d__[resource_key] = resource_value