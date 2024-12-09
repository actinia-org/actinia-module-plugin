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


Test processing
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


from flask import Response
import json
from time import sleep

from actinia_api import URL_PREFIX


from testsuite import ActiniaTestCase, check_started_process


global allTemplatesCount
global templateUUID


class ActiniaProcessingTest(ActiniaTestCase):
    def test_processing(self):
        """Test Usage of global templates persistent processing"""

        respStatusCode = 200
        json_path = "tests/resources/processing/global_default_value.json"
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

    def test_processing_export(self):
        """Test Usage of global templates ephemeral processing"""
        respStatusCode = 200
        json_path = "tests/resources/processing/global_point_in_polygon.json"
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

    def test_processing_if_statement_1(self):
        """
        Test Usage of global templates ephemeral processing with if
        statement where all variables are set"""
        respStatusCode = 200
        json_path = (
            "tests/resources/processing/global_if_statement_filled_all.json"
        )
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

        # poll status until finished
        status = resp.json["status"]
        while status not in ["error", "finished"]:
            sleep(3)
            resp = self.app.get(
                resp.json["urls"]["status"], headers=self.user_auth_header
            )
            status = resp.json["status"]

        # check if parameter is set
        resp.json["process_chain_list"]
        params = [
            param["param"]
            for param in resp.json["process_chain_list"][0]["list"][0][
                "inputs"
            ]
        ]
        assert "region" in params, "Parameter 'region' is not set"

    def test_processing_if_statement_2(self):
        """
        Test Usage of global templates ephemeral processing with if
        statement where the variable in the if statement is not set"""
        respStatusCode = 200
        json_path = (
            "tests/resources/processing/global_if_statement_not_all.json"
        )
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

        # poll status until finished
        status = resp.json["status"]
        while status not in ["error", "finished"]:
            sleep(3)
            resp = self.app.get(
                resp.json["urls"]["status"], headers=self.user_auth_header
            )
            status = resp.json["status"]

        # check if parameter is set
        resp.json["process_chain_list"]
        params = [
            param["param"]
            for param in resp.json["process_chain_list"][0]["list"][0][
                "inputs"
            ]
        ]
        assert "region" not in params, "Parameter 'region' is set"
