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


Test Template CRUD
"""

__license__ = "Apache-2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"


from flask import Response
import json
import uuid

from actinia_core.resources.common.app import URL_PREFIX

from testsuite import ActiniaTestCase


global allTemplatesCount
global templateUUID


class ActiniaTemplatesTest(ActiniaTestCase):

    def test_1_read_all(self):
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        allTemplatesCount = len(resp.json)

    def test_2_create(self):
        global templateUUID

        respStatusCode = 201

        with open('tests/resources/actinia_templates/pc_template.json') as jsonfile:
            pc_template = json.load(jsonfile)
        templateUUID = str(uuid.uuid4())
        pc_template['id'] = templateUUID

        resp = self.app.post(URL_PREFIX + '/actinia_templates',
                             headers=self.user_auth_header,
                             data=json.dumps(pc_template),
                             content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json is True

    def test_3_read_single(self):
        global templateUUID

        respStatusCode = 200

        resp = self.app.get(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        with open('tests/resources/actinia_templates/pc_template.json') as jsonfile:
            pc_template = json.load(jsonfile)
        pc_template['id'] = templateUUID
        assert resp.json == pc_template

    def test_4_update(self):
        global templateUUID

        respStatusCode = 201
        with open('tests/resources/actinia_templates/pc_template2.json') as jsonfile:
            pc_template = json.load(jsonfile)
        pc_template['id'] = templateUUID

        resp = self.app.put(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header,
                            data=json.dumps(pc_template),
                            content_type="application/json")

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json is True

    def test_5_read_update(self):
        global templateUUID

        respStatusCode = 200

        resp = self.app.get(URL_PREFIX + '/actinia_templates/' + templateUUID,
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        with open('tests/resources/actinia_templates/pc_template2.json') as jsonfile:
            pc_template = json.load(jsonfile)
        pc_template['id'] = templateUUID
        assert resp.json == pc_template

    def test_6_read_all_after_create(self):
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        assert len(resp.json) == (allTemplatesCount + 1)

    def test_7_delete(self):
        global templateUUID

        respStatusCode = 200
        resp = self.app.delete(URL_PREFIX + '/actinia_templates/'
                               + templateUUID,
                               headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')
        assert resp.json is True

    def test_8_read_all_after_delete(self):
        global allTemplatesCount

        respStatusCode = 200
        resp = self.app.get(URL_PREFIX + '/actinia_templates',
                            headers=self.user_auth_header)

        assert type(resp) is Response
        assert resp.status_code == respStatusCode
        assert hasattr(resp, 'json')

        assert type(resp.json) is list
        assert len(resp.json) == allTemplatesCount
