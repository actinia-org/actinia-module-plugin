#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 mundialis GmbH & Co. KG

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
__copyright__ = "Copyright 2025, mundialis"

import json
from flask import Response

from actinia_api import URL_PREFIX

from testsuite import (
    ActiniaTestCase,
    check_started_process,
    delete_user_template,
    import_user_template,
)


class ActiniaModulesProcessingTest(ActiniaTestCase):
    def test_process_global_module(self):
        """
        Test HTTP POST /actinia_modules/<module>/processing of
        global templates ephemeral processing
        """
        respStatusCode = 200
        json_path = "tests/resources/processing/global_point_in_polygon.json"
        url_path = "/actinia_modules/point_in_polygon/process"

        with open(json_path) as file:
            pc_template = json.load(file)

        resp = self.app.post(
            URL_PREFIX + url_path,
            headers=self.user_auth_header,
            data=json.dumps(pc_template),
            content_type="application/json",
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")

        check_started_process(self, resp)

    def test_process_user_module(self):
        """
        Test HTTP POST /actinia_modules/<module>/processing of
        user templates ephemeral processing
        """
        import_user_template(self, "user_point_in_polygon")

        respStatusCode = 200
        json_path = (
            "tests/resources/processing/"
            "user_point_in_polygon_actinia_module_process.json"
        )
        url_path = "/actinia_modules/user_point_in_polygon/process"

        with open(json_path) as file:
            pc_template = json.load(file)

        resp = self.app.post(
            URL_PREFIX + url_path,
            headers=self.user_auth_header,
            data=json.dumps(pc_template),
            content_type="application/json",
        )

        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        assert hasattr(resp, "json")

        check_started_process(self, resp)

        delete_user_template(self, "user_point_in_polygon")
