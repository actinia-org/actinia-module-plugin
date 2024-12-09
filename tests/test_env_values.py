#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Test the usage of environment variables
"""

__license__ = "Apache-2.0"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023, mundialis"


from flask import Response
import json
from time import sleep

from actinia_api import URL_PREFIX

from testsuite import (
    ActiniaTestCase,
    check_started_process,
)

global allTemplatesCount
global templateUUID


class ActiniaTestEnvValues(ActiniaTestCase):
    def test_env_values_get(self):
        """Test Usage of environment values inside a template"""

        respStatusCode = 200
        msg = "Default value exist for this installation."

        resp = self.app.get(
            f"{URL_PREFIX}/actinia_modules/use_env_value",
            headers=self.user_auth_header,
        )
        assert isinstance(resp, Response)
        assert (
            resp.status_code == respStatusCode
        ), f"Status code is {resp.status_code} insted of {respStatusCode}"
        params = {
            p["name"]: [p["optional"], p["description"]]
            for p in resp.json["parameters"]
        }
        assert "env_raster" in params, "'env_raster' not in params"
        assert params["env_raster"][
            0
        ], f"{params['env_raster'][0]} is not True"

        assert msg in params["env_raster"][1], "'msg' not in env_raster"

    def test_env_values_processing(self):
        """Test usage of envrionment values in processing procedure"""

        respStatusCode = 200
        json_path = "tests/resources/processing/env_var.json"
        url_path = f"/{self.project_url_part}/nc_spm_08/processing_export"

        with open(json_path) as file:
            pc_template = json.load(file)

        resp = self.app.post(
            URL_PREFIX + url_path,
            headers=self.user_auth_header,
            data=json.dumps(pc_template),
            content_type="application/json",
        )

        assert isinstance(resp, Response), "'resp' is not of class Response"
        assert (
            resp.status_code == respStatusCode
        ), f"Status code is {resp.status_code} insted of {respStatusCode}"
        assert hasattr(resp, "json"), "'resp' has no attribute 'json'"

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
        params = {
            param["param"]: param["value"]
            for param in resp.json["process_chain_list"][0]["list"][0][
                "inputs"
            ]
        }
        assert "type" in params, "Parameter 'type' is set"
        assert params["type"] == "raster", "Parameter 'type' is not 'raster'"

    def test_env_values_processing_overwrite(self):
        """
        Test usage overwriting the envrionment values in processing
        procedure
        """

        respStatusCode = 200
        json_path = "tests/resources/processing/env_var_overwrite.json"
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
        params = {
            param["param"]: param["value"]
            for param in resp.json["process_chain_list"][0]["list"][0][
                "inputs"
            ]
        }
        assert "type" in params, "Parameter 'type' is set"
        assert params["type"] == "vector", "Parameter 'type' is not 'vector'"
