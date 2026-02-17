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

GrassModules = ["r.slope.aspect", "importer", "exporter"]
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
someVirtualModules = GrassModules + someActiniaModules
someActiniaModulesWithExport = [
    "point_in_polygon",
    "slope_aspect",
    # "nested_modules_test",
]


class VirtualModulesTest(ActiniaTestCase):
    def test_list_virtual_modules_get(self):
        """Test HTTP GET /modules"""
        global someVirtualModules

        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules", headers=self.user_auth_header
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert "grass-module" in resp.json["processes"][0]["categories"]
        assert "actinia-module" in resp.json["processes"][-1]["categories"]

        assert len(resp.json["processes"]) > 150
        assert "categories" in resp.json["processes"][0]
        assert "description" in resp.json["processes"][0]
        assert "id" in resp.json["processes"][0]

        respModules = [i["id"] for i in resp.json["processes"]]

        for i in someVirtualModules:
            assert i in respModules

    def test_filter_list_modules_get_admin_1(self):
        """Test HTTP GET /modules with filter as admin"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?category=slope",
            headers=self.admin_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json["processes"]) == 2

    def test_filter_list_modules_get_admin_2(self):
        """Test HTTP GET /modules with filter as admin"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?category=slope&tag=grass",
            headers=self.admin_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json["processes"]) == 2

    def test_filter_list_modules_get_admin_3(self):
        """Test HTTP GET /grass_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?record=full&family=ps",
            headers=self.admin_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json["processes"]) == 1
        assert resp.json["processes"][0]["categories"] != 0
        assert resp.json["processes"][0]["parameters"] != 0

    def test_filter_list_modules_get_user_1(self):
        """Test HTTP GET /modules with filter"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?tag=actinia&category=grass",
            headers=self.user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons. Both importer and exporter are
        # whitelisted and should be found
        assert len(resp.json["processes"]) == 2

    def test_filter_list_modules_get_user_2(self):
        """
        Test HTTP GET /modules with filter as user.
        actinia modules are not whitelisted but available by default.
        """
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?tag=actinia", headers=self.user_auth_header
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons. If kvdb db is empty, it should include
        # all pc_templates from templates/pc_templates including subdirs and
        # importer and exporter.
        num_of_actinia_modules = len(
            [
                x
                for x in resp.json["processes"]
                if x["id"] not in ["exporter", "importer"]
            ]
        )
        assert num_of_actinia_modules >= 7

    def test_filter_list_modules_get_user_3(self):
        """
        Test HTTP GET /modules with filter.
        global actinia modules can be used by any user.
        """
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?tag=actinia&category=global-template",
            headers=self.user_auth_header,
        )
        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json["processes"]) >= 7

    def test_filter_list_modules_get_restricted_user_1(self):
        """Test HTTP GET /modules with filter as restricted user."""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?tag=grass",
            headers=self.restricted_user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert len(resp.json["processes"]) == 3

    def test_filter_list_modules_get_restricted_user_2(self):
        """
        Test HTTP GET /modules with filter as restricted user.
        actinia modules are available by default.
        """
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/modules?tag=actinia",
            headers=self.restricted_user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        num_of_actinia_modules = len(
            [
                x
                for x in resp.json["processes"]
                if x["id"] not in ["exporter", "importer"]
            ]
        )
        assert num_of_actinia_modules >= 7


for i in someVirtualModules:
    """
    Test HTTP GET /modules/<module> for file based templates and GRASS GIS
    modules in loop for all examples in someVirtualModules above and compares
    response to file
    """
    # create method for every actinia-module to have a better overview in
    # test summary
    def_name = "test_describe_virtual_module_get_" + i
    compare_module_to_file.__defaults__ = (
        "modules",
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
    setattr(VirtualModulesTest, def_name, new_func)


for i in someActiniaModulesWithExport:
    """
    Test HTTP GET /modules/<module> with HTTP GET parameter
    """
    # create method for every actinia-module to have a better overview in
    # test summary
    def_name = "test_describe_process_chain_template_get_" + i + "_with_export"
    compare_module_to_file.__defaults__ = (
        "modules",
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
    setattr(VirtualModulesTest, def_name, new_func)
