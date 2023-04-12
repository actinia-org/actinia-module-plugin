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

from actinia_api import URL_PREFIX

from testsuite import (
    ActiniaTestCase,
)

global allTemplatesCount
global templateUUID


class ActiniaTestEnvValues(ActiniaTestCase):
    def test_env_values(self):
        """Test Usage of environment values inside a template"""

        respStatusCode = 200
        msg = "Default value exist for this installation."

        resp = self.app.get(
            URL_PREFIX + "/actinia_modules/use_env_value",
            headers=self.user_auth_header,
        )
        assert isinstance(resp, Response)
        assert resp.status_code == respStatusCode
        params = {
            p["name"]: [p["optional"], p["description"]]
            for p in resp.json["parameters"]
        }
        assert "env_raster" in params
        assert params["env_raster"][0] is True
        assert msg in params["env_raster"][1]
