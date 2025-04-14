#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-2021 mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Code based on actinia_core: github.com/mundialis/actinia_core

# actinia-core - an open source REST API for scalable, distributed, high
# performance processing of geographical data that uses GRASS GIS for
# computational tasks. For details, see https://actinia.mundialis.de/
#
# Copyright (c) 2016-2019 Sören Gebbert and mundialis GmbH & Co. KG
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


Base class for GRASS GIS REST API tests
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika, Sören Gebbert"
__copyright__ = "Copyright 2016-2018, Sören Gebbert, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis"


import base64
from copy import deepcopy
import json
import unittest

import pwgen
from werkzeug.datastructures import Headers

from actinia_core.endpoints import create_endpoints
from actinia_core.core.common.kvdb_interface import connect, disconnect
from actinia_core.core.common.app import flask_app, URL_PREFIX
from actinia_core.core.common.config import global_config
from actinia_core.core.common.process_queue import create_process_queue
from actinia_core.models.response_models import ProcessingResponseModel
from actinia_core.core.common.user import ActiniaUser
from actinia_core.version import init_versions, G_VERSION

# actinia-module-plugin endpoints are included as defined in actinia_core
# config
create_endpoints()


class ActiniaTestCase(unittest.TestCase):
    # guest = None
    # admin = None
    # superadmin = None
    user = None
    auth_header = {}
    users_list = []
    project_url_part = "projects"

    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    def setUp(self):
        """Overwrites method setUp from unittest.TestCase class"""

        self.app_context = flask_app.app_context()
        self.app_context.push()
        # from http://flask.pocoo.org/docs/0.12/api/#flask.Flask.test_client:
        # Note that if you are testing for assertions or exceptions in your
        # application code, you must set app.testing = True in order for the
        # exceptions to propagate to the test client.  Otherwise, the exception
        # will be handled by the application (not visible to the test client)
        # and the only indication of an AssertionError or other exception will
        # be a 500 status code response to the test client.
        flask_app.testing = True
        self.app = flask_app.test_client()

        # Start and connect the kvdb interface
        kvdb_args = (
            global_config.KVDB_SERVER_URL,
            global_config.KVDB_SERVER_PORT,
        )
        if (
            global_config.KVDB_SERVER_PW
            and global_config.KVDB_SERVER_PW is not None
        ):
            kvdb_args = (*kvdb_args, global_config.KVDB_SERVER_PW)
        connect(*kvdb_args)

        # create test user for roles user (more to come)
        accessible_datasets = {
            "nc_spm_08": ["PERMANENT", "user1", "modis_lst"]
        }

        accessible_modules = deepcopy(global_config.MODULE_ALLOW_LIST)
        accessible_modules.extend(["v.db.addcolumn", "v.what.vect"])
        password = pwgen.pwgen()
        (
            self.user_id,
            self.user_group,
            self.user_auth_header,
        ) = self.createUser(
            name="user",
            role="user",
            password=password,
            process_num_limit=30,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
            accessible_modules=accessible_modules,
        )
        (
            self.restricted_user_id,
            self.restricuted_user_group,
            self.restricted_user_auth_header,
        ) = self.createUser(
            name="user2",
            role="user",
            password=password,
            process_num_limit=30,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
            accessible_modules=["v.db.select", "importer", "r.mapcalc"],
        )
        (
            self.admin_id,
            self.admin_group,
            self.admin_auth_header,
        ) = self.createUser(
            name="admin",
            role="admin",
            password=password,
            process_num_limit=30,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
        )

        # create process queue
        create_process_queue(config=global_config)

    def tearDown(self):
        """Overwrites method tearDown from unittest.TestCase class"""

        self.app_context.pop()

        # remove test user; disconnect kvdb
        for user in self.users_list:
            user.delete()
        disconnect()

    def createUser(
        self,
        name="guest",
        role="guest",
        group="group",
        password="abcdefgh",
        accessible_datasets=None,
        accessible_modules=global_config.MODULE_ALLOW_LIST,
        process_num_limit=1000,
        process_time_limit=6000,
        cell_limit=1100000000,
    ):
        auth = bytes("%s:%s" % (name, password), "utf-8")
        # We need to create an HTML basic authorization header
        self.auth_header[role] = Headers()
        self.auth_header[role].add(
            "Authorization", "Basic " + base64.b64encode(auth).decode()
        )

        # Make sure the user database is empty
        user = ActiniaUser(name)
        if user.exists():
            user.delete()
        # Create a user in the database
        user = ActiniaUser.create_user(
            name,
            group,
            password,
            user_role=role,
            accessible_datasets=accessible_datasets,
            accessible_modules=accessible_modules,
            process_num_limit=process_num_limit,
            process_time_limit=process_time_limit,
            cell_limit=cell_limit,
        )
        user.add_accessible_modules(["uname", "sleep"])
        self.users_list.append(user)

        return name, group, self.auth_header[role]


# import unittest
# @unittest.skip("compare response to file")
def compare_module_to_file(self, uri_path="modules", module=None):
    """Compares response of API call to file"""
    # Won't run with module=None but ensures, that "passing of arguments"
    # below is successful.

    resp = self.app.get(
        URL_PREFIX + "/" + uri_path + "/" + module,
        headers=self.user_auth_header,
    )
    respStatusCode = 200
    assert hasattr(resp, "json")
    currentResp = resp.json

    with open("tests/resources/actinia_modules/" + module + ".json") as file:
        expectedResp = json.load(file)

    assert resp.status_code == respStatusCode
    assert currentResp == expectedResp


def import_user_template(testCase, name):
    """Imports user template to kvdb database (Create)"""
    json_path = "tests/resources/actinia_templates/" + name + ".json"
    with open(json_path) as file:
        pc_template = json.load(file)
    resp = testCase.app.post(
        URL_PREFIX + "/actinia_templates",
        headers=testCase.user_auth_header,
        data=json.dumps(pc_template),
        content_type="application/json",
    )
    assert resp.status == "201 CREATED"


def delete_user_template(testCase, name):
    """Deletes user template from kvdb database (Delete) if exists"""
    resp = testCase.app.get(
        URL_PREFIX + "/actinia_templates/" + name,
        headers=testCase.user_auth_header,
    )
    if resp.status_code != 404:
        resp = testCase.app.delete(
            URL_PREFIX + "/actinia_templates/" + name,
            headers=testCase.user_auth_header,
        )
        assert resp.status_code == 200


def check_started_process(testCase, resp):
    """Checks response of started process - TODO: can be enhanced"""
    if isinstance(resp.json["process_results"], dict):
        resp_json = deepcopy(resp.json)
        del resp_json["process_results"]
        resp_json["process_results"] = str(resp.json["process_results"])
    resp_class = ProcessingResponseModel(**resp_json)
    assert resp_class["status"] == "accepted"
    status_url = resp_class["urls"]["status"]

    # poll status_url
    # TODO: status stays in accepted
    status_resp = testCase.app.get(
        status_url, headers=testCase.user_auth_header
    )
    assert status_resp.json["urls"]["status"] == status_url
