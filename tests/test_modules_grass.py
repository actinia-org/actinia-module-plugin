#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Test Module Lists and Self-Description
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


# import unittest

from flask import Response

from actinia_api import URL_PREFIX

from actinia_core.version import init_versions, G_VERSION

from testsuite import ActiniaTestCase, compare_module_to_file


someGrassModules = ["r.slope.aspect", "importer", "exporter"]


class GmodulesTest(ActiniaTestCase):

    # For expected test results, which are dependent on GRASS GIS version
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]

    # @unittest.skip("demonstrating skipping")
    def test_list_modules_get_user(self):
        """Test HTTP GET /grass_modules for user"""
        global someGrassModules

        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/grass_modules", headers=self.user_auth_header
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert len(resp.json["processes"]) > 150
        assert "categories" in resp.json["processes"][0]
        assert "description" in resp.json["processes"][0]
        assert "id" in resp.json["processes"][0]

        respModules = [i["id"] for i in resp.json["processes"]]
        for i in someGrassModules:
            assert i in respModules

    def test_list_modules_get_restricted_user(self):
        """Test HTTP GET /grass_modules for restricted user"""
        global someGrassModules

        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/grass_modules",
            headers=self.restricted_user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        assert len(resp.json["processes"]) == 3
        assert "categories" in resp.json["processes"][0]
        assert "description" in resp.json["processes"][0]
        assert "id" in resp.json["processes"][0]

    def test_filter_list_modules_get_user(self):
        """Test HTTP GET /grass_modules with filter as user"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/grass_modules?category=slope",
            headers=self.user_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        # only r.slope.aspect is permitted
        assert len(resp.json["processes"]) == 1

    def test_filter_list_modules_get_admin(self):
        """Test HTTP GET /grass_modules with filter as admin"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/grass_modules?category=slope",
            headers=self.admin_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        # both r.slope.aspect and v.to.db should be allowed
        assert len(resp.json["processes"]) == 2

    def test_filter_list_modules_get_admin_2(self):
        """Test HTTP GET /grass_modules with filter as admin"""
        respStatusCode = 200
        url_path = "/grass_modules?record=full&family=ps"
        resp = self.app.get(
            URL_PREFIX + url_path, headers=self.admin_auth_header
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        assert len(resp.json["processes"]) == 1
        assert resp.json["processes"][0]["categories"] != 0
        assert resp.json["processes"][0]["parameters"] != 0

    def test_filter_list_modules_get_admin_3(self):
        """Test HTTP GET /grass_modules with filter"""
        respStatusCode = 200
        resp = self.app.get(
            URL_PREFIX + "/grass_modules?family=test",
            headers=self.admin_auth_header,
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")
        # WARNING: this depends on existing GRASS GIS modules and possible
        # installed GRASS GIS Addons
        if self.grass_version < [8, 5]:
            assert len(resp.json["processes"]) == 2
        else:
            assert len(resp.json["processes"]) == 3
        assert resp.json["processes"][0]["categories"] != 0
        assert hasattr(resp.json["processes"][0], "parameters") is False


for i in someGrassModules:
    """
    Test HTTP GET /grass_modules/<module> for GRASS GIS modules in loop
    for all examples in someGrassModules above and compares response to file
    """
    # create method for every grass-module to have a better overview in
    # test summary
    def_name = "test_describe_module_get_" + i
    compare_module_to_file.__defaults__ = (
        "grass_modules",
        i,
    )
    setattr(GmodulesTest, def_name, compare_module_to_file)
