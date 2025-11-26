#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2021-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: Apache-2.0

Test processing
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


from flask import Response
import json

from actinia_api import URL_PREFIX

from testsuite import (
    ActiniaTestCase,
    import_user_template,
    delete_user_template,
    check_started_process,
)


global allTemplatesCount
global templateUUID


class ActiniaProcessingTest(ActiniaTestCase):
    def test_processing(self):
        """Test Usage of user templates persistent processing"""
        import_user_template(self, "user_default_value")

        respStatusCode = 200
        json_path = "tests/resources/processing/user_default_value.json"
        url_path = (
            f"/{self.project_url_part}/nc_spm_08/mapsets/test/processing"
        )

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

        resp = self.app.delete(
            f"{URL_PREFIX}/{self.project_url_part}/nc_spm_08/mapsets/test",
            headers=self.user_auth_header,
        )

        delete_user_template(self, "user_default_value")

    def test_processing_export(self):
        """Test Usage of user templates ephemeral processing"""
        import_user_template(self, "user_point_in_polygon")

        respStatusCode = 200
        json_path = "tests/resources/processing/user_point_in_polygon.json"
        url_path = f"/{self.project_url_part}/nc_spm_08/processing_export"

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
