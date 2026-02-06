#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2021-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Test Module Lists and Self-Description
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


import types
from flask import Response

from actinia_api import URL_PREFIX

from testsuite import ActiniaTestCase, compare_module_to_file


someActiniaModules = [
    "add_enumeration",
    "default_value",
    "nested_modules_test",
    "point_in_polygon",
    "slope_aspect",
    "vector_area",
    "index_NDVI",
    "loop_simple",
    "loop",
]

someActiniaModulesWithExport = [
    "point_in_polygon",
    "slope_aspect",
    # "nested_modules_test",
]


class ActiniaModulesTest(ActiniaTestCase):

    def test_list_modules_get(self):
        """Test HTTP GET /actinia_modules"""
        global someActiniaModules

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + "/actinia_modules")

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert "actinia-module" in resp.json["processes"][0]["categories"]

        respModules = [i["id"] for i in resp.json["processes"]]

        for i in someActiniaModules:
            assert i in respModules

    def test_filter_list_modules_get(self):
        """Test HTTP GET /actinia_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + "/actinia_modules?tag=global")

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert len(resp.json["processes"]) >= 7

    def test_describe_modules_not_found(self):
        """Test HTTP GET /actinia_modules/<not-existing-module>"""
        respStatusCode = 404
        resp = self.app.get(
            URL_PREFIX + "/actinia_modules/not_exist",
            headers=self.user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")


for i in someActiniaModules:
    """
    Test HTTP GET /actinia_modules/<module> for file based templates in loop
    for all examples in someActiniaModules above and compares response to file
    """
    # create method for every actinia-module to have a better overview in
    # test summary
    def_name = "test_describe_process_chain_template_get_" + i
    compare_module_to_file.__defaults__ = (
        "actinia_modules",
        i,
        None,
    )

    new_func = types.FunctionType(
        compare_module_to_file.__code__,
        compare_module_to_file.__globals__,
        name=def_name,
        argdefs=compare_module_to_file.__defaults__,
        closure=compare_module_to_file.__closure__,
    )
    setattr(ActiniaModulesTest, def_name, new_func)


for i in someActiniaModulesWithExport:
    """
    Test HTTP GET /actinia_modules/<module> with HTTP GET parameter
    """
    # create method for every actinia-module to have a better overview in
    # test summary
    def_name = "test_describe_process_chain_template_get_" + i + "_with_export"
    compare_module_to_file.__defaults__ = (
        "actinia_modules",
        i,
        "export",
    )

    new_func = types.FunctionType(
        compare_module_to_file.__code__,
        compare_module_to_file.__globals__,
        name=def_name,
        argdefs=compare_module_to_file.__defaults__,
        closure=compare_module_to_file.__closure__,
    )
    setattr(ActiniaModulesTest, def_name, new_func)
