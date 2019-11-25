#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ResourceLibrary():
    def __init__(self, resource_dictionary):
        self.__d__:dict = resource_dictionary

    def get(self, requested_resource):
        return self.__d__.get(requested_resource).copy() or False

    def set_resource(self, resource_key, resource_value):
        self.__d__[resource_key] = resource_value